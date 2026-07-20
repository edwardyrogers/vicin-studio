import re

_SAFE_FILENAME_RE = re.compile(r"^[\w\s\-\.]+$")
_MAX_FILENAME_LENGTH = 100


def sanitise_filename(filename: str) -> str:
    filename = filename.strip()
    if not filename:
        raise ValueError("Filename must not be empty.")
    if len(filename) > _MAX_FILENAME_LENGTH:
        raise ValueError(
            f"Filename must not exceed {_MAX_FILENAME_LENGTH} characters."
        )
    if not _SAFE_FILENAME_RE.match(filename):
        raise ValueError(
            "Filename contains invalid characters. "
            "Use letters, numbers, spaces, hyphens, and dots only."
        )
    return filename


def validate_content(content: str) -> str:
    if not content or not content.strip():
        raise ValueError("Script content must not be empty.")
    return content
