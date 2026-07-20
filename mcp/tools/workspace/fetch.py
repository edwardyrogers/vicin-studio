from pathlib import Path

from .parse import PLACEHOLDER_SCRIPT, SCRIPT_SUBDIRS


async def init_workspace(project_dir: str) -> dict:
    base = Path(project_dir).resolve()
    script_dir = base / "scripts" / PLACEHOLDER_SCRIPT

    for subdir in SCRIPT_SUBDIRS:
        (script_dir / subdir).mkdir(parents=True, exist_ok=True)

    return {
        "initialized": True,
        "scripts_dir": str(base / "scripts"),
        "placeholder_script": str(script_dir),
    }


async def init_workspace_raw(project_dir: str) -> str:
    """Dry-run: shows what folders would be created without writing anything."""
    base = Path(project_dir).resolve()
    lines = [f"Would create under: {base}", ""]
    for subdir in SCRIPT_SUBDIRS:
        lines.append(f"  scripts/{PLACEHOLDER_SCRIPT}/{subdir}/")
    return "\n".join(lines)
