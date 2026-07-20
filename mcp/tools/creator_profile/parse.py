import json

_REQUIRED_FIELDS = ("niche",)


def parse_profile(raw: str) -> dict:
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"vicin_profile.json is not valid JSON: {e}")

    if not isinstance(data, dict):
        raise ValueError("vicin_profile.json must be a JSON object.")

    missing = [f for f in _REQUIRED_FIELDS if not data.get(f)]
    if missing:
        raise ValueError(
            f"vicin_profile.json is missing required fields: {', '.join(missing)}"
        )

    return data


def format_profile_summary(profile: dict) -> str:
    lines = []
    if profile.get("niche"):
        lines.append(f"Niche: {profile['niche']}")
    if profile.get("target_audience"):
        lines.append(f"Target audience: {profile['target_audience']}")
    return "\n".join(lines)
