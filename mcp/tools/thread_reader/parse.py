import re
from datetime import datetime, timedelta

_RELATIVE_TIME_RE = re.compile(r"\b(\d+)\s*(m|h|d)\b")
_CDN_IMAGE_RE = re.compile(r"https://[^\s]+\.(?:jpg|jpeg|png|webp)", re.IGNORECASE)
_CDN_VIDEO_RE = re.compile(r"https://[^\s]+\.(?:mp4|mov|webm)", re.IGNORECASE)
_COMMENTER_PROFILE_RE = re.compile(r"\]\(https://www\.threads\.com/@([^/?#\)]+)\)")
_ABSOLUTE_DATE_RE = re.compile(r"\[(\d{2}/\d{2}/\d{2})\]")
_MAX_COMMENTS = 10
_STOP_MARKERS = (
    "Related threads",
    "Log in to see more replies",
    "Log in or sign up for Threads",
)


def parse_username(markdown: str, fallback: str) -> str:
    m = re.search(r"@([^\s\)]+)\)\s+on\s+Threads", markdown)
    return m.group(1) if m else fallback


def parse_post_text(markdown: str) -> str:
    split = markdown.split("\nTranslate\n", 1)
    if len(split) < 2:
        raise ValueError("Could not locate post body in page content.")

    pre_block = split[0]
    body_lines: list[str] = []

    for line in pre_block.splitlines():
        stripped = line.strip()
        if re.match(
            r"^(Title:|URL[: ]|Source:|Published:|Description:|Markdown Content:)",
            stripped,
        ):
            continue
        if re.match(r"^={3,}$", stripped):
            continue
        if re.match(r"^\[\]\(", stripped):
            continue
        if re.match(r"^#+\s", stripped):
            continue
        if stripped.startswith("[") and "@" in stripped and "](http" in stripped:
            continue
        body_lines.append(line)

    post_text = re.sub(r"\n{3,}", "\n\n", "\n".join(body_lines)).strip()
    if not post_text:
        raise ValueError("Post text was empty after parsing.")

    post_text = re.sub(r"\[([^@\[\]]+)\]\(https?://[^\)]+\)", r"\1", post_text)
    return post_text


def parse_timestamp(markdown: str) -> str:
    pre_block = markdown.split("\nTranslate\n", 1)[0]

    rel_match = _RELATIVE_TIME_RE.search(pre_block)
    if rel_match:
        value = int(rel_match.group(1))
        unit = rel_match.group(2)
        if unit == "m":
            dt = datetime.utcnow() - timedelta(minutes=value)
        elif unit == "h":
            dt = datetime.utcnow() - timedelta(hours=value)
        else:
            dt = datetime.utcnow() - timedelta(days=value)
        return dt.isoformat()

    date_match = _ABSOLUTE_DATE_RE.search(pre_block)
    if date_match:
        try:
            return datetime.strptime(date_match.group(1), "%m/%d/%y").isoformat()
        except ValueError:
            pass

    return datetime.utcnow().isoformat()


def extract_comments(markdown: str) -> list[str]:
    split = markdown.split("\nTranslate\n", 1)
    if len(split) < 2:
        return []

    post_block = split[1]
    for marker in _STOP_MARKERS:
        idx = post_block.find(marker)
        if idx != -1:
            post_block = post_block[:idx]

    lines = post_block.splitlines()
    comments: list[str] = []
    i = 0

    while i < len(lines) and len(comments) < _MAX_COMMENTS:
        line = lines[i].strip()
        if not line:
            i += 1
            continue

        commenter_match = _COMMENTER_PROFILE_RE.search(line)
        if not commenter_match:
            i += 1
            continue

        commenter = f"@{commenter_match.group(1)}"
        comment_parts: list[str] = []
        i += 1

        while i < len(lines):
            next_line = lines[i].strip()
            if not next_line:
                i += 1
                if comment_parts:
                    break
                continue
            if _COMMENTER_PROFILE_RE.search(next_line):
                break
            if re.match(r"^!?\[", next_line) or re.match(r"^\d+$", next_line):
                i += 1
                continue
            comment_parts.append(next_line)
            i += 1

        if comment_parts:
            comments.append(f"{commenter}: {' '.join(comment_parts)}")

    return comments


def detect_media_type(markdown: str) -> str:
    pre_block = markdown.split("\nTranslate\n", 1)[0]
    if _CDN_VIDEO_RE.search(pre_block):
        return "VIDEO"
    if _CDN_IMAGE_RE.search(pre_block):
        return "IMAGE"
    return "TEXT_POST"
