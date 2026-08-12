"""Local web server for the Council — FastAPI + a vanilla SPA.

`./council` starts this server and opens the browser. One WebSocket carries an
entire run: the browser sends a `start` message with the run spec, the server
drives the pipeline, streams live progress back, pauses for the two human
checkpoints (the browser answers on the same socket), and delivers the final
result. REST endpoints feed the configuration form and serve downloads.

Single active run at a time — you run one council at a time, and that keeps the
state model honest.
"""
from __future__ import annotations

import asyncio
import contextlib
import hashlib
import ipaddress
import json
import math
import os
import re
import secrets
import zipfile
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from cli.agents import load_all_agents, research_agents, process_agents
from cli.config import get_config
from cli.events import WebSink, set_sink
from cli.interactive import (
    AGENT_GROUPS,
    DEFAULT_AUDIENCE,
    DEFAULT_TONE,
    OUTPUT_FORMATS,
    FORMAT_KEYS,
    PRESET_DEFAULT,
    RunSpec,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
WEBAPP_DIR = Path(__file__).resolve().parent / "webapp"
REPORTS_DIR = REPO_ROOT / "reports"

ARGUMENT_UPLOAD_EXTENSIONS = {
    ".pdf", ".docx", ".pptx", ".xlsx", ".md", ".txt", ".csv", ".json",
    ".yaml", ".yml",
}
ARGUMENT_UPLOAD_MAX_FILE_BYTES = 40 * 1024 * 1024
ARGUMENT_UPLOAD_MAX_TOTAL_BYTES = 100 * 1024 * 1024
ARGUMENT_UPLOAD_MAX_FILES = 20
SOURCE_UPLOAD_PURPOSES = {"report", "scope", "argument"}

app = FastAPI(title="Transform Airports AI Council")

# Module-level single-run state.
_active_sink: WebSink | None = None
_active_owner: str | None = None
# Live WebSocket connections per client id. The browser's client id lives in
# sessionStorage, so a crashed or closed tab never comes back under the same
# identity. Without liveness tracking the run's owner would stay a dead tab
# forever and nobody could approve its checkpoints — the run would stall with
# no way to recover but killing the server. Counting sockets lets control pass
# to a live tab once the owner is genuinely gone, while a still-connected owner
# keeps exclusive control and additional tabs remain observers.
_live_clients: dict[str, int] = {}
_SESSION_TOKEN = secrets.token_urlsafe(32)
_SESSION_HEADER = "x-council-session"
_CLIENT_HEADER = "x-council-client"
_CLIENT_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{16,128}$")


def _authority(value: str) -> tuple[str, int | None] | None:
    """Parse a Host header without accepting user-info or path components."""

    if not value or "/" in value or "\\" in value or "@" in value:
        return None
    try:
        parsed = urlsplit(f"//{value}")
        host = (parsed.hostname or "").lower()
        port = parsed.port
    except ValueError:
        return None
    if not host:
        return None
    return host, port


def _is_loopback_name(host: str) -> bool:
    """Only trust the loopback names this app is intended to run on."""

    if host == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _origin_matches_local_host(
    origin: str | None,
    host_header: str | None,
    transport_scheme: str,
) -> bool:
    """Require an exact, loopback same-origin browser request.

    Matching both Origin and Host closes the browser-based localhost attack
    where an unrelated web page attempts to drive this paid local control
    plane. Restricting the host name to loopback also blocks DNS rebinding.
    """

    host_authority = _authority(host_header or "")
    if host_authority is None:
        return False
    host, host_port = host_authority
    if not _is_loopback_name(host):
        return False

    try:
        parsed_origin = urlsplit(origin or "")
        origin_host = (parsed_origin.hostname or "").lower()
        origin_port = parsed_origin.port
    except ValueError:
        return False

    expected_scheme = "https" if transport_scheme in {"https", "wss"} else "http"
    if (
        parsed_origin.scheme != expected_scheme
        or parsed_origin.username is not None
        or parsed_origin.password is not None
        or parsed_origin.path not in {"", "/"}
        or parsed_origin.query
        or parsed_origin.fragment
        or origin_host != host
        or not _is_loopback_name(origin_host)
    ):
        return False

    default_port = 443 if expected_scheme == "https" else 80
    return (origin_port or default_port) == (host_port or default_port)


def _valid_session_token(candidate: object) -> bool:
    return isinstance(candidate, str) and secrets.compare_digest(
        candidate, _SESSION_TOKEN
    )


def _valid_client_id(candidate: object) -> bool:
    return isinstance(candidate, str) and bool(_CLIENT_ID_PATTERN.fullmatch(candidate))


def _http_request_is_authenticated(request: Request) -> bool:
    return (
        _origin_matches_local_host(
            request.headers.get("origin"),
            request.headers.get("host"),
            request.url.scheme,
        )
        and _valid_session_token(request.headers.get(_SESSION_HEADER))
        and _valid_client_id(request.headers.get(_CLIENT_HEADER))
    )


def _websocket_client(socket: WebSocket) -> str | None:
    """Return the authenticated connection identity, or None before accept."""

    client_id = socket.query_params.get("client_id")
    if not (
        _origin_matches_local_host(
            socket.headers.get("origin"),
            socket.headers.get("host"),
            socket.url.scheme,
        )
        and _valid_session_token(socket.query_params.get("token"))
        and _valid_client_id(client_id)
    ):
        return None
    return client_id


def _owner_is_present() -> bool:
    """True only while the run's controlling tab still holds a live socket."""

    return bool(_active_owner) and _live_clients.get(str(_active_owner), 0) > 0


def _run_is_live() -> bool:
    return _active_task is not None and not _active_task.done()


def _control_status(client_id: str) -> dict[str, Any]:
    """Tell a tab whether it can approve checkpoints, and why."""

    controls = _active_owner == client_id
    return {
        "type": "control_status",
        "controls": controls,
        "run_active": _run_is_live(),
        "message": (
            ""
            if controls
            else "Another open tab is controlling this run. Close it to take over."
        ),
    }


def _coerce_budget(value: object) -> float | None:
    """Validate browser-supplied ceilings without turning zero into unlimited."""

    if value is None or value == "":
        return None
    if isinstance(value, bool):
        raise ValueError("Budget must be a finite number, zero or greater.")
    try:
        budget = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            "Budget must be a finite number, zero or greater."
        ) from exc
    if not math.isfinite(budget) or budget < 0:
        raise ValueError("Budget must be a finite number, zero or greater.")
    return budget
_active_task: asyncio.Task | None = None


# ----------------------------------------------------------------------------
# Static + index.
# ----------------------------------------------------------------------------

@app.middleware("http")
async def no_cache(request, call_next):
    """Never let the browser cache the app.

    This is a locally-served tool that gets updated in place. A cached app.js
    against fresh index.html (or vice versa) produces broken, hard-to-diagnose
    UI — e.g. a nav that doesn't know about a view that exists in the markup,
    which blanks the page. Always serve fresh.
    """
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:
    return HTMLResponse((WEBAPP_DIR / "index.html").read_text(encoding="utf-8"))


app.mount("/static", StaticFiles(directory=str(WEBAPP_DIR)), name="static")


# ----------------------------------------------------------------------------
# Metadata for the configuration form.
# ----------------------------------------------------------------------------

@app.get("/api/agents")
async def api_agents() -> JSONResponse:
    agents = load_all_agents()
    by_name = {a.name: a for a in agents}
    groups = []
    for label, names in AGENT_GROUPS:
        members = []
        for name in names:
            a = by_name.get(name)
            if a is None:
                continue
            members.append({
                "name": a.name,
                "display": a.display_name,
                "description": a.description.splitlines()[0].strip() if a.description else "",
                "gated": a.provider != "anthropic",
                "supplemental": a.is_supplemental,
                "default": name in PRESET_DEFAULT,
            })
        groups.append({"label": label, "members": members})
    procs = [
        {"name": a.name, "display": a.display_name,
         "description": a.description.splitlines()[0].strip() if a.description else ""}
        for a in process_agents(agents).values()
    ]
    return JSONResponse({"groups": groups, "process": procs})


@app.get("/api/meta")
async def api_meta(request: Request) -> JSONResponse:
    host_authority = _authority(request.headers.get("host", ""))
    if host_authority is None or not _is_loopback_name(host_authority[0]):
        return JSONResponse({"error": "local access only"}, status_code=403)
    cfg = get_config()
    from cli.menu import check_claude_auth
    from cli.sources import discover_dropzone, format_size
    # The auth check shells out to `claude -p` — run it off the event loop.
    ok, auth_msg = await asyncio.to_thread(check_claude_auth)
    sources = [
        {"name": p.name, "size": format_size(p.stat().st_size)}
        for p in discover_dropzone()
    ]
    return JSONResponse({
        "formats": [{"label": k, "key": FORMAT_KEYS[k], "length": v}
                    for k, v in OUTPUT_FORMATS.items()],
        "default_budget": cfg.default_budget_usd,
        "models": {
            role: cfg.model(role)
            for role in (
                "context", "research", "curation", "creative", "synthesis", "critique",
                "executive_review", "editor", "humanizer", "factcheck",
                "art_direction", "presentation",
            )
        },
        "auth_ok": ok,
        "auth_message": auth_msg,
        "openai_key": bool(os.environ.get("OPENAI_API_KEY")),
        "sources": sources,
        "active_run": bool(_active_task is not None and not _active_task.done()),
        # The browser's same-origin policy protects this per-process token.
        # It authenticates the WebSocket handshake and state-changing requests.
        "session_token": _SESSION_TOKEN,
    })


def _argument_upload_dir(
    client_id: str,
    repo_root: Path | None = None,
    purpose: str = "argument",
) -> Path:
    if not _valid_client_id(client_id):
        raise ValueError("Invalid source-upload client ID.")
    if purpose not in SOURCE_UPLOAD_PURPOSES:
        raise ValueError("Invalid source-upload purpose.")
    root = (repo_root or REPO_ROOT) / "sources" / ".browser-uploads"
    if root.is_symlink():
        raise ValueError("Source upload root may not be a symlink.")
    client_directory = root / client_id
    if client_directory.is_symlink():
        raise ValueError("Source upload client directory may not be a symlink.")
    directory = client_directory / purpose
    if directory.is_symlink():
        raise ValueError("Source upload directory may not be a symlink.")
    return directory


def _safe_argument_upload_name(raw: object) -> str:
    if not isinstance(raw, str):
        raise ValueError("Upload filename is missing.")
    name = raw.strip()
    if (
        not name
        or len(name) > 220
        or Path(name).name != name
        or name.startswith(".")
        or any(ord(character) < 32 for character in name)
    ):
        raise ValueError("Upload filename is unsafe.")
    if Path(name).suffix.lower() not in ARGUMENT_UPLOAD_EXTENSIONS:
        raise ValueError(
            "Unsupported file type. Use PDF, Word, PowerPoint, Excel, Markdown, "
            "text, CSV, JSON, or YAML."
        )
    return name


def _resolve_argument_uploads(
    client_id: str,
    tokens: object,
    repo_root: Path | None = None,
    purpose: str = "argument",
) -> list[Path]:
    if not isinstance(tokens, list) or any(not isinstance(item, str) for item in tokens):
        raise ValueError("Uploaded source tokens must be a list.")
    directory = _argument_upload_dir(client_id, repo_root, purpose)
    if not directory.is_dir():
        if tokens:
            raise ValueError("Uploaded source material is no longer staged.")
        return []
    resolved_root = directory.resolve()
    paths: list[Path] = []
    for token in dict.fromkeys(tokens):
        name = _safe_argument_upload_name(token)
        candidate = directory / name
        if candidate.is_symlink():
            raise ValueError("Uploaded argument material may not be a symlink.")
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(resolved_root)
        except (OSError, ValueError) as exc:
            raise ValueError(f"Uploaded source material is missing: {name}") from exc
        if not resolved.is_file():
            raise ValueError(f"Uploaded source material is not a file: {name}")
        paths.append(candidate)
    return paths


@app.post("/api/source")
@app.post("/api/argument-source")
async def upload_argument_source(
    request: Request,
    name: str = "",
    purpose: str = "argument",
) -> JSONResponse:
    """Stage one browser-selected source without granting arbitrary file access."""

    if not _http_request_is_authenticated(request):
        return JSONResponse({"error": "unauthorized"}, status_code=403)
    try:
        safe_name = _safe_argument_upload_name(name)
        client_id = str(request.headers.get(_CLIENT_HEADER) or "")
        directory = _argument_upload_dir(client_id, purpose=purpose)
        directory.mkdir(parents=True, exist_ok=True)
        existing = [path for path in directory.iterdir() if path.is_file()]
        if len(existing) >= ARGUMENT_UPLOAD_MAX_FILES:
            raise ValueError(f"Attach no more than {ARGUMENT_UPLOAD_MAX_FILES} files.")
        existing_bytes = sum(path.stat().st_size for path in existing)
        target = directory / safe_name
        if target.exists() or target.is_symlink():
            stem, suffix = Path(safe_name).stem, Path(safe_name).suffix
            number = 2
            while (directory / f"{stem}-{number}{suffix}").exists():
                number += 1
            target = directory / f"{stem}-{number}{suffix}"
        temporary = directory / f".{secrets.token_urlsafe(12)}.upload"
        written = 0
        try:
            with temporary.open("xb") as handle:
                async for chunk in request.stream():
                    written += len(chunk)
                    if written > ARGUMENT_UPLOAD_MAX_FILE_BYTES:
                        raise ValueError("One attachment exceeds the 40 MB file limit.")
                    if existing_bytes + written > ARGUMENT_UPLOAD_MAX_TOTAL_BYTES:
                        raise ValueError("Attachments exceed the 100 MB total limit.")
                    handle.write(chunk)
            if written == 0:
                raise ValueError("The uploaded file is empty.")
            os.replace(temporary, target)
        finally:
            if temporary.exists():
                temporary.unlink()
        from cli.sources import format_size

        return JSONResponse(
            {"token": target.name, "name": target.name, "size": format_size(written)}
        )
    except (OSError, ValueError) as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)


@app.delete("/api/source")
@app.delete("/api/argument-source")
async def delete_argument_source(
    request: Request,
    token: str = "",
    purpose: str = "argument",
) -> JSONResponse:
    if not _http_request_is_authenticated(request):
        return JSONResponse({"error": "unauthorized"}, status_code=403)
    try:
        client_id = str(request.headers.get(_CLIENT_HEADER) or "")
        path = _resolve_argument_uploads(client_id, [token], purpose=purpose)[0]
        path.unlink()
        return JSONResponse({"removed": token})
    except (OSError, ValueError, IndexError) as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)


# ----------------------------------------------------------------------------
# The run WebSocket.
# ----------------------------------------------------------------------------

async def _drive_new(spec: RunSpec, sink: WebSink, auto_approve: bool,
                     budget_usd: float | None) -> None:
    from cli.orchestrator import run_pipeline
    from cli.runfile import write_run_file
    run_file = write_run_file(spec)
    result = await run_pipeline(
        spec=spec, run_file=run_file, repo_root=REPO_ROOT,
        auto_approve=auto_approve, budget_usd=budget_usd,
    )
    if not result.completed:
        await sink.emit("run_stopped", {"total": result.tally.total})


async def _drive_scope(payload: dict, sink: WebSink) -> None:
    from cli.scope import run_scope_pipeline
    client_id = str(payload.get("client_id") or "")
    source_files = _resolve_argument_uploads(
        client_id,
        payload.get("source_tokens") or [],
        REPO_ROOT,
        purpose="scope",
    )
    result = await run_scope_pipeline(
        title=payload.get("title") or "Scope engagement",
        notes=payload.get("notes", ""),
        source_files=source_files,
        repo_root=REPO_ROOT,
        auto_approve=bool(payload.get("auto_approve")),
        budget_usd=payload.get("budget"),
    )
    if not result.completed:
        await sink.emit("run_stopped", {"total": result.tally.total})


async def _drive_strengthen(payload: dict, sink: WebSink) -> None:
    from cli.strengthen import StrengthenRequest, run_strengthen_pipeline

    allowed = {agent.name for agent in research_agents(load_all_agents())}
    request = StrengthenRequest.from_payload(payload, allowed_agents=allowed)
    client_id = str(payload.get("client_id") or "")
    source_files = _resolve_argument_uploads(
        client_id, request.source_tokens, REPO_ROOT
    )
    result = await run_strengthen_pipeline(
        request=request,
        source_files=source_files,
        repo_root=REPO_ROOT,
        budget_usd=payload.get("budget"),
    )
    if not result.completed:
        await sink.emit("run_stopped", {"total": result.tally.total})


async def _drive_resume(slug: str, sink: WebSink, auto_approve: bool,
                        budget_usd: float | None) -> None:
    from cli.orchestrator import read_run_marker, run_pipeline
    from cli.runfile import RUNS_DIR, parse_run_file
    # Scope engagements resume through the scope pipeline, keyed by the marker.
    marker = read_run_marker(REPO_ROOT / "outputs") or {}
    if marker.get("mode") == "scope":
        from cli.scope import run_scope_pipeline
        result = await run_scope_pipeline(
            title=marker.get("title") or slug, repo_root=REPO_ROOT,
            source_files=(), auto_approve=auto_approve, budget_usd=budget_usd,
        )
        if not result.completed:
            await sink.emit("run_stopped", {"total": result.tally.total})
        return
    if marker.get("mode") == "strengthen":
        from cli.strengthen import load_strengthen_request, run_strengthen_pipeline

        allowed = {agent.name for agent in research_agents(load_all_agents())}
        request_path = REPO_ROOT / "outputs" / str(
            marker.get("request") or "context/argument-request.json"
        )
        request = load_strengthen_request(request_path, allowed)
        result = await run_strengthen_pipeline(
            request=request,
            source_files=(),
            repo_root=REPO_ROOT,
            budget_usd=budget_usd,
            resume=True,
        )
        if not result.completed:
            await sink.emit("run_stopped", {"total": result.tally.total})
        return
    spec = parse_run_file(slug)
    run_file = RUNS_DIR / f"{slug}.md"
    result = await run_pipeline(
        spec=spec, run_file=run_file, repo_root=REPO_ROOT,
        auto_approve=auto_approve, budget_usd=budget_usd, resume=True,
    )
    if not result.completed:
        await sink.emit("run_stopped", {"total": result.tally.total})


async def _drive_revise(slug: str, feedback: str, sink: WebSink, auto_approve: bool) -> None:
    from cli.orchestrator import run_revision_pipeline
    from cli.revise import revisable_reports, next_revision_version

    # Build the request without the interactive picker.
    src = next((s for s in revisable_reports() if s.slug == slug), None)
    if src is None:
        await sink.emit("run_error", {"message": f"No revisable report '{slug}'."})
        return
    from cli.revise import RevisionRequest
    version = next_revision_version(src.archive_dir)
    request = RevisionRequest(source=src, feedback=feedback, version=version)
    out_path, tally = await run_revision_pipeline(
        request=request, repo_root=REPO_ROOT, auto_approve=auto_approve,
    )
    if out_path is not None:
        release_slug = f"{slug}-revised-v{version}"
        await sink.emit("run_complete", {
            "slug": release_slug,
            "revise_slug": slug,
            "title": f"{slug} — Revised v{version}",
            "total": tally.total,
            "revision": version,
            "mode": "revision",
        })
    else:
        await sink.emit("run_stopped", {"total": tally.total})


async def _drive_deck(
    slug: str,
    sink: WebSink,
    budget_usd: float | None,
) -> None:
    from cli.orchestrator import run_presentation_for_archive
    from cli.publish import discover_reports
    src = next((s for s in discover_reports() if s.slug == slug), None)
    if src is None:
        await sink.emit("run_error", {"message": f"No archived run '{slug}'."})
        return
    title = slug.replace("-", " ").title()
    if src.run_file is not None:
        for line in src.run_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            if line.startswith("# Run:"):
                title = line[len("# Run:"):].strip()
                break
    await sink.emit("run_start", {"slug": slug, "title": f"{title} — deck",
                                  "agents": ["art-director", "presentation-designer"],
                                  "mode": "deck"})
    await sink.emit("stage_start", {"stage": 4, "label": "Art direction, design, and QA"})
    await run_presentation_for_archive(
        archive_dir=src.archive_dir,
        slug=slug,
        title=title,
        repo_root=REPO_ROOT,
        budget_usd=budget_usd,
    )
    backfill_manifest = (
        src.archive_dir / "stage4" / f"{slug}-deck-backfill.json"
    )
    try:
        claude_total = float(
            json.loads(
                backfill_manifest.read_text(encoding="utf-8")
            ).get("claude_cost_usd")
            or 0.0
        )
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        claude_total = max(
            (
                float(event.get("total") or 0.0)
                for event in sink.agent_events.values()
            ),
            default=0.0,
        )
    await sink.emit("run_complete", {
        "slug": slug,
        "title": f"{title} — deck",
        "total": claude_total,
    })


async def _drive_run(mode: str, payload: dict, sink: WebSink) -> None:
    """Dispatch a run by mode inside this task's context with the sink active."""
    from cli.runfile import ensure_unique_slug

    set_sink(sink)
    auto_approve = bool(payload.get("auto_approve"))
    try:
        budget = _coerce_budget(payload.get("budget"))
        if mode == "scope":
            await _drive_scope({**payload, "budget": budget}, sink)
        elif mode == "strengthen":
            await _drive_strengthen({**payload, "budget": budget}, sink)
        elif mode == "resume":
            await _drive_resume(payload["slug"], sink, auto_approve, budget)
        elif mode == "revise":
            await _drive_revise(payload["slug"], payload.get("feedback", ""), sink, auto_approve)
        elif mode == "deck":
            await _drive_deck(payload["slug"], sink, budget)
        else:  # new
            spec = _build_spec(payload.get("spec", {}))
            spec.slug = ensure_unique_slug(spec.slug)
            # Attach only the files selected for this browser workflow.
            from cli.sources import attach_sources
            source_files = _resolve_argument_uploads(
                str(payload.get("client_id") or ""),
                payload.get("spec", {}).get("source_tokens") or [],
                REPO_ROOT,
                purpose="report",
            )
            if source_files:
                attached = attach_sources(spec.slug, source_files, REPO_ROOT / "outputs")
                spec.source_paths = [
                    s.readable.relative_to(REPO_ROOT).as_posix() for s in attached
                ]
            await _drive_new(spec, sink, auto_approve, budget)
    except Exception as e:  # noqa: BLE001 — surface to the browser
        await sink.emit("run_error", {"message": f"{type(e).__name__}: {e}"})
    finally:
        await sink.close()


def _build_spec(data: dict) -> RunSpec:
    from slugify import slugify
    title = (data.get("title") or "Untitled Run").strip()
    fmt = data.get("output_format") or "report"
    length = next((v for k, v in OUTPUT_FORMATS.items() if FORMAT_KEYS[k] == fmt),
                  OUTPUT_FORMATS["Full Research Report (4,000–6,000 words)"])
    scope = [s.strip() for s in (data.get("scope") or []) if s.strip()]
    avoid = [s.strip() for s in (data.get("avoid") or []) if s.strip()]
    return RunSpec(
        title=title,
        slug=slugify(title) or "untitled-run",
        thesis=(data.get("thesis") or "").strip(),
        audience=data.get("audience") or DEFAULT_AUDIENCE,
        tone=data.get("tone") or DEFAULT_TONE,
        length=length,
        output_format=fmt,
        is_not=avoid or ["A vendor pitch for any specific platform or product"],
        is_yes=(scope[:1] + ["A sharp, evidence-driven argument that earns its conclusions"])
        if scope else ["A sharp, evidence-driven argument that earns its conclusions"],
        success_criteria=scope or ["Every numerical claim traces to a primary source"],
        operator_context=(data.get("operator_context") or "").strip(),
        decision_required=(data.get("decision_required") or "").strip(),
        decision_owner=(data.get("decision_owner") or "").strip(),
        time_horizon=(data.get("time_horizon") or "").strip(),
        approval_path=(data.get("approval_path") or "").strip(),
        success_measure=(data.get("success_measure") or "").strip(),
        selected_research_agents=list(data.get("agents") or []),
        want_pptx=bool(data.get("want_pptx")),
        deck_mode=(
            data.get("deck_mode")
            if data.get("deck_mode") in {
                "board_decision", "executive_briefing", "technical_read_ahead"
            }
            else "board_decision"
        ),
    )


@app.websocket("/ws")
async def ws(socket: WebSocket) -> None:
    global _active_owner, _active_sink, _active_task
    connection_client = _websocket_client(socket)
    if connection_client is None:
        # Reject the handshake before accepting a browser-controlled channel.
        await socket.close(code=1008)
        return
    await socket.accept()
    _live_clients[connection_client] = _live_clients.get(connection_client, 0) + 1
    pump: asyncio.Task | None = None
    try:
        while True:
            raw = await socket.receive_text()
            try:
                msg = json.loads(raw)
            except json.JSONDecodeError:
                await socket.send_json({
                    "type": "control_error",
                    "message": "Malformed control message.",
                })
                continue
            if not isinstance(msg, dict) or not (
                _valid_session_token(msg.get("session_token"))
                and msg.get("client_id") == connection_client
            ):
                await socket.send_json({
                    "type": "control_error",
                    "message": "This control message is not authenticated.",
                })
                continue
            mtype = msg.get("type")

            if mtype == "start":
                if _active_task is not None and not _active_task.done():
                    await socket.send_json({"type": "run_error",
                                            "message": "A run is already in progress."})
                    continue
                sink = WebSink()
                _active_sink = sink
                _active_owner = connection_client
                _active_task = asyncio.create_task(
                    _drive_run(msg.get("mode", "new"), msg, sink)
                )
                if pump is not None:
                    pump.cancel()
                await socket.send_json(_control_status(connection_client))
                pump = asyncio.create_task(_pump(sink, socket))

            elif mtype == "attach":
                if not _run_is_live() or _active_sink is None:
                    await socket.send_json({
                        "type": "run_error",
                        "message": "No active run is available to attach.",
                    })
                    continue
                # A crashed or closed tab must not hold control forever. If the
                # owner has no live socket, hand control to this tab so the run
                # can be approved and finished rather than stalling at its next
                # checkpoint. A still-connected owner keeps exclusive control.
                if not _owner_is_present():
                    _active_owner = connection_client
                await socket.send_json(_control_status(connection_client))
                cursor = msg.get("after")
                cursor = int(cursor) if isinstance(cursor, int) and cursor > 0 else 0
                if pump is not None:
                    pump.cancel()
                pump = asyncio.create_task(_pump(_active_sink, socket, cursor))

            elif mtype == "checkpoint":
                if _active_owner != connection_client:
                    if _owner_is_present():
                        await socket.send_json({
                            "type": "control_error",
                            "message": "This tab is observing the run and cannot approve it.",
                        })
                        continue
                    # The controlling tab is gone; this live tab takes over
                    # rather than leaving the run stalled at its checkpoint.
                    _active_owner = connection_client
                    await socket.send_json(_control_status(connection_client))
                if (
                    _active_task is None
                    or _active_task.done()
                    or _active_sink is None
                ):
                    await socket.send_json({
                        "type": "control_error",
                        "message": "No active checkpoint is available.",
                    })
                    continue
                _active_sink.resolve(msg.get("id"), {
                    "action": msg.get("action"),
                    "notes": msg.get("notes", ""),
                    "ratings": msg.get("ratings", {}),
                })

            elif mtype == "cancel":
                if _active_owner != connection_client:
                    if _owner_is_present():
                        await socket.send_json({
                            "type": "control_error",
                            "message": "This tab is observing the run and cannot cancel it.",
                        })
                        continue
                    _active_owner = connection_client
                    await socket.send_json(_control_status(connection_client))
                if _active_task is not None and not _active_task.done():
                    _active_task.cancel()
                else:
                    await socket.send_json({
                        "type": "control_error",
                        "message": "No active run is available to cancel.",
                    })

    except WebSocketDisconnect:
        pass
    finally:
        remaining = _live_clients.get(connection_client, 0) - 1
        if remaining > 0:
            _live_clients[connection_client] = remaining
        else:
            _live_clients.pop(connection_client, None)
        if pump is not None:
            pump.cancel()


async def _pump(sink: WebSink, socket: WebSocket, cursor: int = 0) -> None:
    """Replay and follow the sequenced event log without duplicate delivery.

    A re-attaching browser passes the last sequence it rendered, so a reconnect
    costs only the events it actually missed. A fresh attach passes 0 and gets
    the full run replayed.
    """
    while True:
        events = await sink.wait_after(cursor)
        if not events and sink.closed:
            return
        for event in events:
            cursor = max(cursor, int(event.get("seq", 0)))
            with contextlib.suppress(Exception):
                await socket.send_json(event)
            if event.get("type") == "stream_end":
                return


# ----------------------------------------------------------------------------
# Reports + downloads.
# ----------------------------------------------------------------------------

_DOWNLOAD_LABELS = {
    "argument": "Strengthened argument",
    "word_memo": "One-page Word memo",
    "word_report": "Word report",
    "executive_summary": "Executive summary",
    "presentation": "Presentation",
}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _safe_report_path(relative: object, reports_dir: Path) -> Path | None:
    """Resolve a manifest/download path beneath reports/ without traversal."""

    if not isinstance(relative, str) or not relative or "\x00" in relative:
        return None
    raw = Path(relative)
    if raw.is_absolute():
        return None
    root = reports_dir.resolve()
    candidate = (root / raw).resolve()
    try:
        candidate.relative_to(root)
    except ValueError:
        return None
    return candidate


def _safe_scope_distribution_path(
    relative: object,
    reports_dir: Path,
    *,
    expect_directory: bool = False,
) -> Path | None:
    """Resolve a Scope distribution path and reject every symlink component."""

    if not isinstance(relative, str):
        return None
    raw = Path(relative)
    candidate = _safe_report_path(relative, reports_dir)
    if candidate is None:
        return None
    root = reports_dir.resolve()
    lexical = root / raw
    current = lexical
    while current != root:
        if current.is_symlink():
            return None
        current = current.parent
    if expect_directory:
        return candidate if candidate.is_dir() else None
    return candidate if candidate.is_file() else None


def _scope_tree_inventory(root: Path) -> list[dict[str, object]] | None:
    """Return exact Scope package membership, failing closed on links."""

    if root.is_symlink() or not root.is_dir():
        return None
    inventory: list[dict[str, object]] = []
    try:
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                return None
            if not path.is_file():
                continue
            inventory.append(
                {
                    "path": path.relative_to(root).as_posix(),
                    "sha256": _sha256(path),
                    "size_bytes": path.stat().st_size,
                }
            )
    except OSError:
        return None
    return inventory


def _verified_scope_package(
    slug: str,
    reports_dir: Path | None = None,
) -> dict[str, object] | None:
    """Verify one Scope pointer, receipt, package tree, and ZIP exactly."""

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", slug):
        return None
    root = (reports_dir or REPORTS_DIR).resolve()
    pointer_path = root / f"scope-{slug}-package-manifest.json"
    if pointer_path.is_symlink() or not pointer_path.is_file():
        return None
    try:
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        if (
            pointer.get("schema_version") != "1.0"
            or pointer.get("status") != "current"
            or pointer.get("mode") != "scope"
            or pointer.get("slug") != slug
        ):
            return None
        receipt_record = pointer.get("receipt")
        zip_record = pointer.get("zip")
        package_record = pointer.get("package")
        if not all(
            isinstance(item, dict)
            for item in (receipt_record, zip_record, package_record)
        ):
            return None
        receipt_path = _safe_scope_distribution_path(
            receipt_record.get("path"), root
        )
        zip_path = _safe_scope_distribution_path(zip_record.get("path"), root)
        package_dir = _safe_scope_distribution_path(
            package_record.get("path"), root, expect_directory=True
        )
        if receipt_path is None or zip_path is None or package_dir is None:
            return None
        receipt_hash = str(receipt_record.get("sha256") or "")
        zip_hash = str(zip_record.get("sha256") or "")
        if (
            not re.fullmatch(r"[0-9a-f]{64}", receipt_hash)
            or not secrets.compare_digest(_sha256(receipt_path), receipt_hash)
            or not re.fullmatch(r"[0-9a-f]{64}", zip_hash)
            or not secrets.compare_digest(_sha256(zip_path), zip_hash)
            or zip_record.get("size_bytes") != zip_path.stat().st_size
            or zip_path.suffix.lower() != ".zip"
        ):
            return None
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        inventory = _scope_tree_inventory(package_dir)
        if (
            inventory is None
            or receipt.get("schema_version") != "1.0"
            or receipt.get("slug") != slug
            or receipt.get("files") != inventory
            or package_record.get("files") != inventory
            or receipt.get("zip", {}).get("path")
            != zip_path.relative_to(root).as_posix()
            or receipt.get("zip", {}).get("sha256") != zip_hash
            or receipt.get("zip", {}).get("size_bytes")
            != zip_path.stat().st_size
        ):
            return None
        with zipfile.ZipFile(zip_path) as archive:
            names = [info.filename for info in archive.infolist()]
        expected_names = [str(item["path"]) for item in inventory]
        if (
            len(names) != len(set(names))
            or sorted(names) != sorted(expected_names)
        ):
            return None
        return {
            "slug": slug,
            "title": str(pointer.get("title") or slug.replace("-", " ").title()),
            "date": str(pointer.get("date") or ""),
            "zip_path": zip_path.relative_to(root).as_posix(),
            "zip_url": (
                f"/download/{quote(zip_path.relative_to(root).as_posix(), safe='/')}"
            ),
            "deliverables": (
                pointer.get("deliverables")
                if isinstance(pointer.get("deliverables"), list)
                else []
            ),
        }
    except (
        OSError,
        TypeError,
        ValueError,
        KeyError,
        json.JSONDecodeError,
        zipfile.BadZipFile,
    ):
        return None


def _scope_package_for_download(
    relative: str,
    reports_dir: Path | None = None,
) -> bool:
    """Authorize only ZIPs named by a valid Scope distribution pointer."""

    root = (reports_dir or REPORTS_DIR).resolve()
    for pointer in root.glob("scope-*-package-manifest.json"):
        match = re.fullmatch(
            r"scope-(.+)-package-manifest\.json", pointer.name
        )
        if not match:
            continue
        package = _verified_scope_package(match.group(1), root)
        if package and package["zip_path"] == relative:
            return True
    return False


def _verified_argument_release(
    public_slug: str,
    reports_dir: Path | None = None,
) -> dict[str, object] | None:
    """Verify the concise-argument release pointer and every published byte."""

    if not re.fullmatch(r"argument-[A-Za-z0-9][A-Za-z0-9._-]*", public_slug):
        return None
    root = (reports_dir or REPORTS_DIR).resolve()
    pointer_path = root / f"{public_slug}-release.json"
    if pointer_path.is_symlink() or not pointer_path.is_file():
        return None
    try:
        payload = json.loads(pointer_path.read_text(encoding="utf-8"))
        schema_version = str(payload.get("schema_version") or "")
        if (
            schema_version not in {"1.0", "2.0"}
            or payload.get("status") != "current"
            or payload.get("mode") != "strengthen"
            or payload.get("slug") != public_slug
            or not isinstance(payload.get("artifacts"), list)
        ):
            return None
        artifacts: list[dict[str, str]] = []
        roles: set[str] = set()
        for record in payload["artifacts"]:
            if not isinstance(record, dict):
                return None
            role = str(record.get("role") or "")
            expected = str(record.get("sha256") or "")
            path = _safe_scope_distribution_path(record.get("path"), root)
            if (
                role not in {"argument", "word_memo", "presentation"}
                or role in roles
                or path is None
                or not re.fullmatch(r"[0-9a-f]{64}", expected)
                or not secrets.compare_digest(_sha256(path), expected)
                or path.stat().st_size != record.get("size_bytes")
                or (role == "argument" and path.suffix.lower() != ".md")
                or (role == "word_memo" and path.suffix.lower() != ".docx")
                or (role == "presentation" and path.suffix.lower() != ".pptx")
            ):
                return None
            roles.add(role)
            relative = path.relative_to(root).as_posix()
            artifacts.append(
                {
                    "role": role,
                    "label": _DOWNLOAD_LABELS[role],
                    "path": relative,
                    "url": f"/download/{quote(relative, safe='/')}",
                }
            )
        if "argument" not in roles or (
            schema_version == "2.0" and "word_memo" not in roles
        ):
            return None
        argument_record = next(item for item in artifacts if item["role"] == "argument")
        argument_path = root / argument_record["path"]
        return {
            "slug": public_slug,
            "source_slug": str(payload.get("source_slug") or ""),
            "title": str(payload.get("title") or public_slug.replace("-", " ").title()),
            "date": str(payload.get("date") or ""),
            "argument_path": argument_path,
            "memo_path": (
                root
                / next(item for item in artifacts if item["role"] == "word_memo")[
                    "path"
                ]
                if "word_memo" in roles
                else None
            ),
            "artifacts": artifacts,
        }
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return None


def _argument_download_is_current(
    relative: str, reports_dir: Path | None = None
) -> bool:
    root = (reports_dir or REPORTS_DIR).resolve()
    for pointer in root.glob("argument-*-release.json"):
        match = re.fullmatch(r"(argument-.+)-release\.json", pointer.name)
        if not match:
            continue
        release = _verified_argument_release(match.group(1), root)
        if release and any(
            item["path"] == relative for item in release["artifacts"]
        ):
            return True
    return False


def _verified_release_artifacts(
    slug: str,
    reports_dir: Path | None = None,
    *,
    manifest_name: str | None = None,
) -> list[dict[str, str]] | None:
    """Read the current pointer and return only its hash-bound deliverables.

    ``None`` means no current-manifest filename exists, which permits the
    explicit legacy fallback. Any malformed, stale, or mismatched manifest
    fails closed as an empty list.
    """

    root = (reports_dir or REPORTS_DIR).resolve()
    pointer_filename = manifest_name or f"{slug}-release-manifest.json"
    if Path(pointer_filename).name != pointer_filename:
        return []
    pointer_path = root / pointer_filename
    if not pointer_path.is_file():
        return None
    try:
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        if (
            pointer.get("status") != "current"
            or str(pointer.get("slug") or "") != slug
            or not isinstance(pointer.get("artifacts"), list)
        ):
            return []

        bundle_path = _safe_report_path(pointer.get("bundle_path"), root)
        source_manifest_hash = str(
            pointer.get("source_release_manifest_sha256") or ""
        )
        if (
            bundle_path is None
            or not bundle_path.is_file()
            or not re.fullmatch(r"[0-9a-f]{64}", source_manifest_hash)
            or not secrets.compare_digest(
                _sha256(bundle_path), source_manifest_hash
            )
        ):
            return []
        bundle = json.loads(bundle_path.read_text(encoding="utf-8"))
        if (
            bundle.get("status") != "ready"
            or str(bundle.get("slug") or "") != slug
            or not isinstance(bundle.get("artifacts"), list)
        ):
            return []
        # Authorize downloads from the complete immutable bundle, not just the
        # two convenience files named by the pointer. This revalidates every
        # release-required render and the hash-bound visual-inspection receipt;
        # altering or deleting that evidence withdraws the deck immediately.
        from cli.publish import verify_release_bundle

        require_word_report = any(
            isinstance(item, dict)
            and str(item.get("role") or "") == "word_report"
            for item in bundle["artifacts"]
        )
        try:
            verify_release_bundle(
                bundle_path.parent,
                require_word_report=require_word_report,
            )
        except (OSError, RuntimeError, ValueError, json.JSONDecodeError):
            return []
        bundled_by_role = {
            str(item.get("role") or ""): item
            for item in bundle["artifacts"]
            if isinstance(item, dict) and item.get("role")
        }
        if len(bundled_by_role) != len(bundle["artifacts"]):
            return []

        verified: list[dict[str, str]] = []
        seen_roles: set[str] = set()
        for artifact in pointer["artifacts"]:
            if not isinstance(artifact, dict):
                return []
            role = str(artifact.get("role") or "")
            expected = str(artifact.get("sha256") or "")
            candidate = _safe_report_path(artifact.get("path"), root)
            qa_path = _safe_report_path(artifact.get("qa_path"), root)
            qa_hash = str(artifact.get("qa_sha256") or "")
            bundled = bundled_by_role.get(role)
            if (
                not role
                or role in seen_roles
                or bundled is None
                or candidate is None
                or not candidate.is_file()
                or candidate.suffix.lower() not in {".docx", ".pptx"}
                or not re.fullmatch(r"[0-9a-f]{64}", expected)
                or not secrets.compare_digest(_sha256(candidate), expected)
                or str(bundled.get("sha256") or "") != expected
                or artifact.get("qa_ok") is not True
                or bundled.get("qa_ok") is not True
                or qa_path is None
                or not qa_path.is_file()
                or not re.fullmatch(r"[0-9a-f]{64}", qa_hash)
                or not secrets.compare_digest(_sha256(qa_path), qa_hash)
                or str(bundled.get("qa_sha256") or "") != qa_hash
            ):
                return []
            seen_roles.add(role)
            relative = candidate.relative_to(root).as_posix()
            verified.append({
                "role": role,
                "label": _DOWNLOAD_LABELS.get(
                    role, role.replace("_", " ").title()
                ),
                "path": relative,
                "url": f"/download/{quote(relative, safe='/')}",
            })
        return verified
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return []


def _legacy_downloads(
    slug: str,
    reports_dir: Path | None = None,
) -> list[dict[str, str]]:
    """Constrained compatibility path for pre-manifest releases only."""

    root = (reports_dir or REPORTS_DIR).resolve()
    if (
        (root / f"{slug}-release-manifest.json").exists()
        or (root / f"{slug}-deck-release-manifest.json").exists()
    ):
        return []
    candidates = (
        ("word_report", root / f"{slug}.docx"),
        ("executive_summary", root / f"{slug}-executive-summary.docx"),
        ("presentation", root / f"{slug}.pptx"),
    )
    return [
        {
            "role": role,
            "label": _DOWNLOAD_LABELS[role],
            "path": path.name,
            "url": f"/download/{quote(path.name)}",
        }
        for role, path in candidates
        if path.is_file()
    ]


def _downloads_for_slug(
    slug: str,
    reports_dir: Path | None = None,
) -> list[dict[str, str]]:
    canonical = _verified_release_artifacts(slug, reports_dir)
    supplemental = _verified_release_artifacts(
        slug,
        reports_dir,
        manifest_name=f"{slug}-deck-release-manifest.json",
    )
    if canonical is None and supplemental is None:
        return _legacy_downloads(slug, reports_dir)

    merged = list(canonical or [])
    present_roles = {item["role"] for item in merged}
    for artifact in supplemental or []:
        # A backfill pointer is supplemental by contract. It can add a deck,
        # but cannot supersede a role committed by the canonical release.
        if (
            artifact["role"] == "presentation"
            and artifact["role"] not in present_roles
        ):
            merged.append(artifact)
            present_roles.add(artifact["role"])
    return merged


def _verified_revision_report(
    slug: str,
    sources: list[object],
) -> dict[str, object] | None:
    """Resolve a released revision and verify its archived reader-facing body."""

    from cli.revise import _completed_revisions

    match = re.fullmatch(r"(.+)-revised-v([1-9][0-9]*)", slug)
    if not match:
        return None
    source_slug, version_text = match.groups()
    version = int(version_text)
    source = next(
        (
            candidate
            for candidate in sources
            if getattr(candidate, "slug", None) == source_slug
        ),
        None,
    )
    if source is None:
        return None
    if version not in _completed_revisions(Path(source.archive_dir)):
        return None
    base = Path(source.archive_dir) / "revisions" / f"v{version}"
    manifest_path = base / "revision-manifest.json"
    final_draft = base / "final-draft.md"
    release_manifest = base / "release" / "release-manifest.json"
    execution_state = base / "revision-execution.json"
    stage4_report = base / "stage4" / f"{slug}.docx"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        required_hashes = (
            (final_draft, manifest.get("final_draft_sha256")),
            (base / "claim-lineage.jsonl", manifest.get("claim_lineage_sha256")),
            (base / "quality-gate.json", manifest.get("quality_gate_sha256")),
            (stage4_report, manifest.get("word_report_sha256")),
            (release_manifest, manifest.get("release_manifest_sha256")),
            (execution_state, manifest.get("revision_execution_sha256")),
        )
        if (
            manifest.get("schema_version") != "1.0"
            or manifest.get("status") != "released"
            or manifest.get("slug") != source_slug
            or manifest.get("revision") != version
            or any(
                not path.is_file()
                or not isinstance(expected, str)
                or not re.fullmatch(r"[0-9a-f]{64}", expected)
                or not secrets.compare_digest(_sha256(path), expected)
                for path, expected in required_hashes
            )
        ):
            return None
        downloads = _downloads_for_slug(slug)
        if not any(item["role"] == "word_report" for item in downloads):
            return None
        return {
            "slug": slug,
            "source_slug": source_slug,
            "revision": version,
            "created_at": str(manifest.get("created_at") or ""),
            "final_draft": final_draft,
            "downloads": downloads,
        }
    except (OSError, TypeError, ValueError, json.JSONDecodeError):
        return None


def _scope_home_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    if not REPORTS_DIR.is_dir():
        return entries
    for pointer in sorted(REPORTS_DIR.glob("scope-*-package-manifest.json")):
        match = re.fullmatch(
            r"scope-(.+)-package-manifest\.json", pointer.name
        )
        if not match:
            continue
        package = _verified_scope_package(match.group(1))
        if package is None:
            continue
        entries.append(
            {
                "slug": package["slug"],
                "title": package["title"],
                "date": package["date"],
                "format": "scope engagement",
                "mode": "scope",
                "downloads": [
                    {
                        "label": "All deliverables",
                        "url": package["zip_url"],
                    }
                ],
                "revisions": 0,
                "has_deck": False,
                "can_read": False,
                "can_revise": False,
                "can_build_deck": False,
            }
        )
    return entries


def _argument_home_entries() -> list[dict[str, object]]:
    entries: list[dict[str, object]] = []
    if not REPORTS_DIR.is_dir():
        return entries
    for pointer in sorted(REPORTS_DIR.glob("argument-*-release.json")):
        match = re.fullmatch(r"(argument-.+)-release\.json", pointer.name)
        if not match:
            continue
        release = _verified_argument_release(match.group(1))
        if release is None:
            continue
        entries.append(
            {
                "slug": release["slug"],
                "title": release["title"],
                "date": release["date"],
                "format": "one-page argument memo",
                "mode": "strengthen",
                "downloads": [
                    {
                        "label": _DOWNLOAD_LABELS[item["role"]],
                        "url": item["url"],
                    }
                    for item in release["artifacts"]
                ],
                "revisions": 0,
                "has_deck": any(
                    item["role"] == "presentation" for item in release["artifacts"]
                ),
                "can_read": True,
                "can_revise": False,
                "can_build_deck": False,
            }
        )
    return entries


def _legacy_slug_for_download(name: str) -> str | None:
    """Recognize only the three historical top-level deliverable names."""

    if "/" in name or "\\" in name:
        return None
    if name.endswith("-executive-summary.docx"):
        slug = name[: -len("-executive-summary.docx")]
    elif name.endswith(".docx"):
        slug = name[:-len(".docx")]
    elif name.endswith(".pptx"):
        slug = name[:-len(".pptx")]
    else:
        return None
    return slug if slug and re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", slug) else None


def _download_is_current_artifact(
    relative: str,
    reports_dir: Path | None = None,
) -> bool:
    """Authorize an exact path from any valid current distribution pointer."""

    root = (reports_dir or REPORTS_DIR).resolve()
    for pointer in root.glob("*-release-manifest.json"):
        try:
            pointer_payload = json.loads(pointer.read_text(encoding="utf-8"))
        except (OSError, TypeError, json.JSONDecodeError):
            continue
        slug = str(pointer_payload.get("slug") or "")
        declared = pointer_payload.get("artifacts")
        if (
            not slug
            or not isinstance(declared, list)
            or not any(
                isinstance(item, dict) and item.get("path") == relative
                for item in declared
            )
        ):
            continue
        artifacts = _verified_release_artifacts(
            slug,
            root,
            manifest_name=pointer.name,
        )
        if artifacts and any(item["path"] == relative for item in artifacts):
            return True
    return False


@app.get("/api/report/{slug}")
async def api_report(slug: str) -> JSONResponse:
    """The published report's markdown body + available downloads."""
    from cli.publish import discover_reports

    argument_release = _verified_argument_release(slug)
    if argument_release is not None:
        return JSONResponse(
            {
                "slug": slug,
                "revise_slug": None,
                "mode": "strengthen",
                "markdown": Path(argument_release["argument_path"]).read_text(
                    encoding="utf-8", errors="ignore"
                ),
                "downloads": [
                    {"label": item["label"], "url": item["url"]}
                    for item in argument_release["artifacts"]
                ],
            }
        )

    sources = discover_reports()
    final_md = ""
    source = next(
        (candidate for candidate in sources if candidate.slug == slug),
        None,
    )
    if source is not None and source.final_md is not None:
        final_md = source.final_md.read_text(encoding="utf-8", errors="ignore")
        verified_downloads = _downloads_for_slug(slug)
        revise_slug = slug
    else:
        revision = _verified_revision_report(slug, sources)
        if revision is None:
            verified_downloads = []
            revise_slug = slug
        else:
            final_md = Path(revision["final_draft"]).read_text(
                encoding="utf-8", errors="ignore"
            )
            verified_downloads = list(revision["downloads"])
            revise_slug = str(revision["source_slug"])
    downloads = [
        {"label": item["label"], "url": item["url"]}
        for item in verified_downloads
    ]
    return JSONResponse(
        {
            "slug": slug,
            "revise_slug": revise_slug,
            "markdown": final_md,
            "downloads": downloads,
        }
    )


@app.get("/api/home")
async def api_home() -> JSONResponse:
    """Interrupted-run detection + the library of completed reports."""
    from cli.menu import detect_interrupted_run
    from cli.publish import discover_reports
    from cli.revise import next_revision_version

    interrupted = detect_interrupted_run()
    sources = discover_reports()
    archives = []
    for s in sources:
        if s.final_md is None:
            continue
        date = s.archive_dir.name[:10]
        title = s.slug.replace("-", " ").title()
        fmt = "report"
        if s.run_file is not None:
            text = s.run_file.read_text(encoding="utf-8", errors="ignore")
            for line in text.splitlines():
                if line.startswith("# Run:"):
                    title = line[len("# Run:"):].strip()
                    break
            from cli.publish import _detect_format
            fmt = _detect_format(s)
        verified_downloads = _downloads_for_slug(s.slug)
        downloads = [
            {
                "label": (
                    "Word"
                    if item["role"] == "word_report"
                    else "Deck"
                    if item["role"] == "presentation"
                    else item["label"]
                ),
                "url": item["url"],
            }
            for item in verified_downloads
        ]
        revs = next_revision_version(s.archive_dir) - 1
        archives.append({
            "slug": s.slug, "title": title, "date": date, "format": fmt,
            "downloads": downloads, "revisions": revs,
            "mode": "report",
            "revise_slug": s.slug,
            "can_read": True,
            "can_revise": True,
            "can_build_deck": True,
            "has_deck": any(
                item["role"] == "presentation"
                for item in verified_downloads
            ),
        })
        for version in range(1, revs + 1):
            release_slug = f"{s.slug}-revised-v{version}"
            revision = _verified_revision_report(release_slug, sources)
            if revision is None:
                continue
            revision_downloads = [
                {
                    "label": (
                        "Word"
                        if item["role"] == "word_report"
                        else "Deck"
                        if item["role"] == "presentation"
                        else item["label"]
                    ),
                    "url": item["url"],
                }
                for item in revision["downloads"]
            ]
            created_at = str(revision.get("created_at") or "")
            archives.append(
                {
                    "slug": release_slug,
                    "title": f"{title} — Revised v{version}",
                    "date": created_at[:10] or date,
                    "format": fmt,
                    "downloads": revision_downloads,
                    "revisions": 0,
                    "mode": "revision",
                    "revise_slug": s.slug,
                    "can_read": True,
                    "can_revise": True,
                    "can_build_deck": False,
                    "has_deck": any(
                        item["role"] == "presentation"
                        for item in revision["downloads"]
                    ),
                }
            )
    archives.extend(_scope_home_entries())
    archives.extend(_argument_home_entries())
    archives.sort(key=lambda a: a["date"], reverse=True)
    return JSONResponse({
        "interrupted": ({"slug": interrupted["slug"], "title": interrupted["title"],
                         "where": interrupted["where"], "age": interrupted["age"]}
                        if interrupted and interrupted.get("slug") else None),
        "archives": archives,
    })


@app.get("/api/guide")
async def api_guide() -> JSONResponse:
    """The run-prompt writing guide, served from docs/ so it never drifts."""
    path = REPO_ROOT / "docs" / "writing-effective-run-prompts.md"
    md = path.read_text(encoding="utf-8", errors="ignore") if path.is_file() else "Guide not found."
    return JSONResponse({"markdown": md})


@app.get("/api/audit")
async def api_audit() -> JSONResponse:
    from cli.audit import audit_runs, render_audit_report
    agents = load_all_agents()
    report = render_audit_report(audit_runs(agents=agents), agents)
    return JSONResponse({"markdown": report})


@app.post("/api/review/{slug}")
async def api_quality_review(
    slug: str,
    request: Request,
    payload: dict,
) -> JSONResponse:
    """Store an optional human quality signal beside the archived run."""
    if not _http_request_is_authenticated(request):
        return JSONResponse({"error": "forbidden"}, status_code=403)

    from cli.evaluation import write_human_review
    from cli.publish import discover_reports

    archive = next(
        (
            path
            for path in sorted((REPO_ROOT / "runs").glob("*"), reverse=True)
            if path.is_dir() and len(path.name) > 11 and path.name[11:] == slug
        ),
        None,
    )
    if archive is None:
        sources = discover_reports()
        revision = _verified_revision_report(slug, sources)
        if revision is not None:
            source = next(
                (
                    candidate
                    for candidate in sources
                    if candidate.slug == revision["source_slug"]
                ),
                None,
            )
            if source is not None:
                archive = (
                    source.archive_dir
                    / "revisions"
                    / f"v{revision['revision']}"
                )
    if archive is None:
        return JSONResponse({"error": "run not found"}, status_code=404)
    ratings = payload.get("ratings", {})
    if not isinstance(ratings, dict):
        return JSONResponse({"error": "ratings must be an object"}, status_code=400)
    try:
        path = write_human_review(
            archive,
            ratings,
            notes=str(payload.get("notes", "")).strip() or None,
            review_id="final-product",
        )
    except ValueError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    return JSONResponse({"saved": str(path.relative_to(archive))})


@app.get("/download/{name:path}")
async def download(name: str) -> FileResponse:
    """Serve only a verified current artifact or a constrained legacy file."""

    safe = _safe_report_path(name, REPORTS_DIR)
    if safe is None or not safe.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)
    relative = safe.relative_to(REPORTS_DIR.resolve()).as_posix()
    authorized = _download_is_current_artifact(relative)
    if not authorized:
        authorized = _scope_package_for_download(relative)
    if not authorized:
        authorized = _argument_download_is_current(relative)
    if not authorized:
        slug = _legacy_slug_for_download(relative)
        authorized = bool(
            slug
            and any(
                item["path"] == relative
                for item in _legacy_downloads(slug)
            )
        )
    if not authorized:
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(str(safe), filename=safe.name)


def serve(host: str = "127.0.0.1", port: int = 8723, open_browser: bool = True) -> None:
    """Launch the server and open the browser."""
    import uvicorn

    if open_browser:
        import threading
        import webbrowser

        def _open() -> None:
            import time
            time.sleep(1.0)
            webbrowser.open(f"http://{host}:{port}/")

        threading.Thread(target=_open, daemon=True).start()

    uvicorn.run(app, host=host, port=port, log_level="warning")
