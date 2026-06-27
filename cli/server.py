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
import json
import os
from pathlib import Path

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
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

app = FastAPI(title="Transform Airports AI Council")

# Module-level single-run state.
_active_sink: WebSink | None = None
_active_task: asyncio.Task | None = None


# ----------------------------------------------------------------------------
# Static + index.
# ----------------------------------------------------------------------------

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
async def api_meta() -> JSONResponse:
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
        "models": {role: cfg.model(role) for role in
                   ("research", "synthesis", "critique", "editor", "humanizer", "factcheck")},
        "auth_ok": ok,
        "auth_message": auth_msg,
        "openai_key": bool(os.environ.get("OPENAI_API_KEY")),
        "sources": sources,
    })


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


async def _drive_resume(slug: str, sink: WebSink, auto_approve: bool,
                        budget_usd: float | None) -> None:
    from cli.orchestrator import run_pipeline
    from cli.runfile import RUNS_DIR, parse_run_file
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
    from cli.revise import collect_revision_request, revisable_reports, next_revision_version
    from cli.publish import discover_reports

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
        await sink.emit("run_complete", {
            "slug": slug, "title": f"{slug} — Revised v{version}",
            "total": tally.total, "revision": version,
        })
    else:
        await sink.emit("run_stopped", {"total": tally.total})


async def _drive_deck(slug: str, sink: WebSink) -> None:
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
                                  "agents": ["presentation-designer"], "mode": "deck"})
    await sink.emit("stage_start", {"stage": 4, "label": "Designing the deck"})
    await run_presentation_for_archive(
        archive_dir=src.archive_dir, slug=slug, title=title, repo_root=REPO_ROOT,
    )
    await sink.emit("run_complete", {"slug": slug, "title": f"{title} — deck", "total": 0.0})


async def _drive_run(mode: str, payload: dict, sink: WebSink) -> None:
    """Dispatch a run by mode inside this task's context with the sink active."""
    from cli.runfile import ensure_unique_slug

    set_sink(sink)
    auto_approve = bool(payload.get("auto_approve"))
    budget = payload.get("budget")
    try:
        if mode == "resume":
            await _drive_resume(payload["slug"], sink, auto_approve, budget)
        elif mode == "revise":
            await _drive_revise(payload["slug"], payload.get("feedback", ""), sink, auto_approve)
        elif mode == "deck":
            await _drive_deck(payload["slug"], sink)
        else:  # new
            spec = _build_spec(payload.get("spec", {}))
            spec.slug = ensure_unique_slug(spec.slug)
            # Attach any staged source files.
            from cli.sources import discover_dropzone, attach_sources
            dropped = discover_dropzone()
            if dropped and payload.get("spec", {}).get("use_sources", True):
                attached = attach_sources(spec.slug, dropped, REPO_ROOT / "outputs")
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
        selected_research_agents=list(data.get("agents") or []),
        want_pptx=bool(data.get("want_pptx")),
    )


@app.websocket("/ws")
async def ws(socket: WebSocket) -> None:
    global _active_sink, _active_task
    await socket.accept()
    pump: asyncio.Task | None = None
    try:
        while True:
            raw = await socket.receive_text()
            msg = json.loads(raw)
            mtype = msg.get("type")

            if mtype == "start":
                if _active_task is not None and not _active_task.done():
                    await socket.send_json({"type": "run_error",
                                            "message": "A run is already in progress."})
                    continue
                sink = WebSink()
                _active_sink = sink
                _active_task = asyncio.create_task(
                    _drive_run(msg.get("mode", "new"), msg, sink)
                )
                pump = asyncio.create_task(_pump(sink, socket))

            elif mtype == "checkpoint":
                if _active_sink is not None:
                    _active_sink.resolve(msg.get("id"), {
                        "action": msg.get("action"),
                        "notes": msg.get("notes", ""),
                    })

            elif mtype == "cancel":
                if _active_task is not None and not _active_task.done():
                    _active_task.cancel()

    except WebSocketDisconnect:
        pass
    finally:
        if pump is not None:
            pump.cancel()


async def _pump(sink: WebSink, socket: WebSocket) -> None:
    """Drain the sink's event queue to the browser until the run ends."""
    while True:
        event = await sink.queue.get()
        if event.get("type") == "stream_end":
            with contextlib.suppress(Exception):
                await socket.send_json({"type": "stream_end"})
            return
        with contextlib.suppress(Exception):
            await socket.send_json(event)


# ----------------------------------------------------------------------------
# Reports + downloads.
# ----------------------------------------------------------------------------

@app.get("/api/report/{slug}")
async def api_report(slug: str) -> JSONResponse:
    """The published report's markdown body + available downloads."""
    # Find the dated archive for this slug.
    runs_dir = REPO_ROOT / "runs"
    final_md = ""
    if runs_dir.is_dir():
        for d in sorted(runs_dir.iterdir(), reverse=True):
            if d.is_dir() and d.name.endswith(slug):
                fp = d / "stage3" / "final-draft.md"
                if fp.is_file():
                    final_md = fp.read_text(encoding="utf-8", errors="ignore")
                break
    downloads = []
    for suffix, label in ((".docx", "Word report"),
                          ("-executive-summary.docx", "Executive summary"),
                          (".pptx", "Presentation")):
        f = REPORTS_DIR / f"{slug}{suffix}"
        if f.is_file():
            downloads.append({"label": label, "url": f"/download/{f.name}"})
    return JSONResponse({"slug": slug, "markdown": final_md, "downloads": downloads})


@app.get("/api/home")
async def api_home() -> JSONResponse:
    """Interrupted-run detection + the library of completed reports."""
    from cli.menu import detect_interrupted_run
    from cli.publish import discover_reports
    from cli.revise import next_revision_version

    interrupted = detect_interrupted_run()
    archives = []
    for s in discover_reports():
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
        downloads = []
        for suffix, label in ((".docx", "Word"), (".pptx", "Deck")):
            f = REPORTS_DIR / f"{s.slug}{suffix}"
            if f.is_file():
                downloads.append({"label": label, "url": f"/download/{f.name}"})
        revs = next_revision_version(s.archive_dir) - 1
        archives.append({
            "slug": s.slug, "title": title, "date": date, "format": fmt,
            "downloads": downloads, "revisions": revs,
            "has_deck": (REPORTS_DIR / f"{s.slug}.pptx").is_file(),
        })
    archives.sort(key=lambda a: a["date"], reverse=True)
    return JSONResponse({
        "interrupted": ({"slug": interrupted["slug"], "title": interrupted["title"],
                         "where": interrupted["where"], "age": interrupted["age"]}
                        if interrupted and interrupted.get("slug") else None),
        "archives": archives,
    })


@app.get("/api/audit")
async def api_audit() -> JSONResponse:
    from cli.audit import audit_runs, render_audit_report
    agents = load_all_agents()
    report = render_audit_report(audit_runs(agents=agents), agents)
    return JSONResponse({"markdown": report})


@app.get("/download/{name}")
async def download(name: str) -> FileResponse:
    # Constrain to reports/ — never serve arbitrary paths.
    safe = (REPORTS_DIR / name).resolve()
    if not str(safe).startswith(str(REPORTS_DIR.resolve())) or not safe.is_file():
        return JSONResponse({"error": "not found"}, status_code=404)
    return FileResponse(str(safe), filename=name)


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
