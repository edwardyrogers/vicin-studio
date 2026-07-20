import json
from pathlib import Path

from .parse import format_profile_summary, parse_profile

_PROFILE_FILENAME = "vicin_profile.json"


async def fetch_creator_profile(project_dir: str) -> dict:
    profile_path = Path(project_dir).resolve() / _PROFILE_FILENAME

    if not profile_path.exists():
        return {
            "error": (
                f"No {_PROFILE_FILENAME} found in {project_dir}. "
                "Create one to set your creator profile."
            )
        }

    raw = profile_path.read_text(encoding="utf-8")

    try:
        profile = parse_profile(raw)
    except ValueError as e:
        return {"error": str(e)}

    return {
        "profile": profile,
        "summary": format_profile_summary(profile),
        "path": str(profile_path),
    }


async def fetch_creator_profile_raw(project_dir: str) -> str:
    profile_path = Path(project_dir).resolve() / _PROFILE_FILENAME

    if not profile_path.exists():
        return f"No {_PROFILE_FILENAME} found in {project_dir}."

    return profile_path.read_text(encoding="utf-8")


async def save_creator_profile(profile_json: str, project_dir: str) -> dict:
    try:
        profile = parse_profile(profile_json)
    except ValueError as e:
        return {"error": str(e)}

    profile_path = Path(project_dir).resolve() / _PROFILE_FILENAME
    profile_path.write_text(
        json.dumps(profile, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "saved": True,
        "path": str(profile_path),
        "summary": format_profile_summary(profile),
    }


async def save_creator_profile_raw(profile_json: str, project_dir: str) -> str:
    """Dry-run: shows where the profile would be saved without writing."""
    try:
        profile = parse_profile(profile_json)
        profile_path = Path(project_dir).resolve() / _PROFILE_FILENAME
        serialised = json.dumps(profile, ensure_ascii=False, indent=2)
    except ValueError as e:
        return f"Validation error: {e}"
    return f"Would write to: {profile_path}\n\nContent:\n{serialised}"
