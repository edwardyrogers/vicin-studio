def validate_content(content: str) -> str:
    if not content or not content.strip():
        raise ValueError("Guide content must not be empty.")
    return content
