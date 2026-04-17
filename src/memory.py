"""Loads and combines user personal data from local markdown files."""

from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def _read(filename: str) -> str:
    path = DATA_DIR / filename
    if path.exists():
        return path.read_text(encoding="utf-8").strip()
    return ""


def _read_writing_samples() -> str:
    samples_dir = DATA_DIR / "writing_samples"
    if not samples_dir.exists():
        return ""
    texts = []
    for f in sorted(samples_dir.glob("*.md")):
        content = f.read_text(encoding="utf-8").strip()
        if content:
            texts.append(content)
    return "\n\n---\n\n".join(texts)


def load_user_context() -> dict:
    """Return a dict of all personal context sections."""
    return {
        "profile": _read("profile.md"),
        "skills": _read("skills.md"),
        "projects": _read("projects.md"),
        "stories": _read("stories.md"),
        "writing_samples": _read_writing_samples(),
    }


def format_context_block(ctx: dict) -> str:
    """Flatten all sections into a single prompt-ready string."""
    sections = [
        ("PERSONAL PROFILE", ctx["profile"]),
        ("SKILLS", ctx["skills"]),
        ("PROJECTS", ctx["projects"]),
        ("STAR STORIES & ACHIEVEMENTS", ctx["stories"]),
    ]
    parts = []
    for title, body in sections:
        if body:
            parts.append(f"=== {title} ===\n{body}")
    return "\n\n".join(parts)


def format_style_block(ctx: dict) -> str:
    """Return writing samples formatted for style analysis."""
    if not ctx["writing_samples"]:
        return ""
    return f"=== MY PAST WRITING SAMPLES ===\n{ctx['writing_samples']}"
