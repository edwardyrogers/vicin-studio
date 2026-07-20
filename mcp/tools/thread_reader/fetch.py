import re

import httpx

from .parse import (
    detect_media_type,
    extract_comments,
    parse_post_text,
    parse_timestamp,
    parse_username,
)

_THREADS_URL_RE = re.compile(
    r"^https://www\.threads\.com/@([^/?#]+)/post/([A-Za-z0-9_-]+)"
)
_JINA_BASE_URL = "https://r.jina.ai/"
_JINA_HEADERS = {
    "Accept": "text/plain",
    "X-No-Cache": "true",
    "X-Engine": "browser",
}
_INVALID_URL_MSG = (
    "Please provide a valid Threads post URL, "
    "e.g. https://www.threads.com/@username/post/ABC123"
)


def _parse_url(url: str) -> tuple[str, str, str] | None:
    m = _THREADS_URL_RE.match(url.strip())
    if not m:
        return None
    username = m.group(1)
    shortcode = m.group(2)
    canonical = f"https://www.threads.com/@{username}/post/{shortcode}"
    return username, shortcode, canonical


async def _jina_get(canonical_url: str) -> httpx.Response:
    async with httpx.AsyncClient(timeout=30.0) as client:
        return await client.get(
            f"{_JINA_BASE_URL}{canonical_url}",
            headers=_JINA_HEADERS,
        )


async def fetch_thread(url: str) -> dict:
    parsed = _parse_url(url)
    if not parsed:
        return {"error": _INVALID_URL_MSG}

    username_from_url, _, canonical_url = parsed
    response = await _jina_get(canonical_url)

    if response.status_code != 200:
        return {
            "error": (
                f"Could not fetch the post (status {response.status_code}). "
                "The post may be private or unavailable."
            )
        }

    markdown = response.text

    try:
        post_text = parse_post_text(markdown)
    except ValueError as e:
        return {"error": str(e), "raw_preview": markdown[:500]}

    return {
        "username": parse_username(markdown, username_from_url),
        "post_text": post_text,
        "timestamp": parse_timestamp(markdown),
        "media_type": detect_media_type(markdown),
        "permalink": canonical_url,
        "top_comments": extract_comments(markdown),
    }


async def fetch_thread_raw(url: str) -> str:
    parsed = _parse_url(url)
    if not parsed:
        return _INVALID_URL_MSG

    _, _, canonical_url = parsed
    response = await _jina_get(canonical_url)
    return response.text
