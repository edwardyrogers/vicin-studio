from pathlib import Path

from .parse import validate_content

_GUIDE_FILENAME = "CLAUDE.md"


def _resolve_target(project_dir: str) -> Path:
    base = Path(project_dir).resolve()
    target = (base / _GUIDE_FILENAME).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        raise ValueError("Project guide must not escape the project directory.")
    return target


async def save_project_guide(content: str, project_dir: str) -> dict:
    try:
        clean_content = validate_content(content)
        target = _resolve_target(project_dir)
    except ValueError as e:
        return {"error": str(e)}

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean_content, encoding="utf-8")

    return {
        "saved": True,
        "path": str(target),
        "characters": len(clean_content),
    }


async def save_project_guide_raw(content: str, project_dir: str) -> str:
    """Dry-run: shows where CLAUDE.md would be saved without writing anything."""
    try:
        clean_content = validate_content(content)
        target = _resolve_target(project_dir)
    except ValueError as e:
        return f"Validation error: {e}"

    preview = clean_content[:500] + ("..." if len(clean_content) > 500 else "")
    return f"Would write to: {target}\n\nContent preview:\n{preview}"
