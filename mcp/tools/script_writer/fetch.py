from pathlib import Path

from .parse import sanitise_filename, validate_content

_SCRIPTS_SUBFOLDER = "scripts"


def _resolve_target(filename: str, project_dir: str) -> Path:
    base = (Path(project_dir).resolve() / _SCRIPTS_SUBFOLDER).resolve()
    target = (base / filename).resolve()
    try:
        target.relative_to(base)
    except ValueError:
        raise ValueError("Filename must not escape the project directory.")
    return target


async def save_script(filename: str, content: str, project_dir: str) -> dict:
    try:
        clean_filename = sanitise_filename(filename)
        clean_content = validate_content(content)
        target = _resolve_target(clean_filename, project_dir)
    except ValueError as e:
        return {"error": str(e)}

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean_content, encoding="utf-8")

    return {
        "saved": True,
        "path": str(target),
        "filename": clean_filename,
        "characters": len(clean_content),
    }


async def save_script_raw(filename: str, content: str, project_dir: str) -> str:
    """Dry-run: shows where the script would be saved without writing anything."""
    try:
        clean_filename = sanitise_filename(filename)
        clean_content = validate_content(content)
        target = _resolve_target(clean_filename, project_dir)
    except ValueError as e:
        return f"Validation error: {e}"

    preview = clean_content[:500] + ("..." if len(clean_content) > 500 else "")
    return f"Would write to: {target}\n\nContent preview:\n{preview}"
