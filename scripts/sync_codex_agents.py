#!/usr/bin/env python3
"""Mirror `.claude/agents/*.md` into Codex `.codex/agents/*.toml`.

The markdown files remain the human-edited source of truth. This generated
mirror lets the same Council roles appear as native Codex subagents without a
second prompt-maintenance surface.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import frontmatter


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIR = REPO_ROOT / ".claude" / "agents"
TARGET_DIR = REPO_ROOT / ".codex" / "agents"


def _toml_string(value: str) -> str:
    """A JSON string is also a valid TOML basic string."""
    return json.dumps(value, ensure_ascii=False)


def render(path: Path) -> str:
    post = frontmatter.load(path)
    name = str(post.metadata.get("name") or path.stem).strip()
    description = str(post.metadata.get("description") or "").strip()
    body = post.content.strip()
    return "\n".join(
        (
            f"name = {_toml_string(name)}",
            f"description = {_toml_string(description)}",
            f"developer_instructions = {_toml_string(body)}",
            "",
        )
    )


def sync_agents(
    *,
    source_dir: Path = SOURCE_DIR,
    target_dir: Path = TARGET_DIR,
    check: bool = False,
) -> tuple[bool, list[str]]:
    """Synchronize mirrors, or report drift without writing in check mode."""

    sources = sorted(source_dir.glob("*.md"))
    if not sources:
        raise ValueError(f"No agent definitions found in {source_dir}")
    expected = {
        target_dir / f"{source.stem}.toml": render(source)
        for source in sources
    }
    existing = set(target_dir.glob("*.toml")) if target_dir.is_dir() else set()
    messages: list[str] = []
    for target, content in expected.items():
        current = (
            target.read_text(encoding="utf-8", errors="replace")
            if target.is_file()
            else None
        )
        if current != content:
            messages.append(f"out of sync: {target.name}")
    for stale in sorted(existing - set(expected)):
        messages.append(f"stale mirror: {stale.name}")

    if check:
        return not messages, messages

    target_dir.mkdir(parents=True, exist_ok=True)
    for target, content in expected.items():
        if not target.is_file() or target.read_text(
            encoding="utf-8", errors="replace"
        ) != content:
            target.write_text(content, encoding="utf-8")
    for stale in existing - set(expected):
        stale.unlink()
    return True, messages


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate Codex-native TOML mirrors from the human-edited "
            ".claude/agents Markdown definitions."
        )
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Report drift and exit non-zero without changing files.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = _parse_args(argv)
    try:
        clean, messages = sync_agents(check=args.check)
    except ValueError as exc:
        print(exc)
        return 2
    if args.check:
        if clean:
            print(f"Codex mirrors are current ({len(list(SOURCE_DIR.glob('*.md')))} agents).")
            return 0
        print("\n".join(messages))
        return 1
    print(
        f"Synced {len(list(SOURCE_DIR.glob('*.md')))} agents to "
        f"{TARGET_DIR.relative_to(REPO_ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
