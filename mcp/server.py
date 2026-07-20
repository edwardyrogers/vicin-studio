import json

from mcp.server.fastmcp import FastMCP

from tools.creator_profile import (
    fetch_creator_profile,
    fetch_creator_profile_raw,
    save_creator_profile,
    save_creator_profile_raw,
)
from tools.project_guide import save_project_guide, save_project_guide_raw
from tools.workspace import init_workspace, init_workspace_raw
from tools.script_writer import save_script, save_script_raw
from tools.thread_reader import fetch_thread, fetch_thread_raw

mcp = FastMCP("Vicin Studio")


# ── Trend Fetcher ─────────────────────────────────────────────────────────────

@mcp.tool()
async def vicin_fetch_trend_post(url: str) -> str:
    """Fetch a Threads post and return its content and top comments."""
    result = await fetch_thread(url)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def vicin_fetch_trend_post_raw(url: str) -> str:
    """Return raw Jina markdown for a Threads post — used to debug comment parsing."""
    return await fetch_thread_raw(url)


# ── Creator Profile ───────────────────────────────────────────────────────────

@mcp.tool()
async def vicin_fetch_creator_profile(project_dir: str) -> str:
    """Read the creator profile from vicin_profile.json in the given project directory."""
    result = await fetch_creator_profile(project_dir)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def vicin_fetch_creator_profile_raw(project_dir: str) -> str:
    """Return the raw contents of vicin_profile.json — used to debug profile parsing."""
    return await fetch_creator_profile_raw(project_dir)


@mcp.tool()
async def vicin_save_creator_profile(profile_json: str, project_dir: str) -> str:
    """Save a creator profile JSON string to vicin_profile.json in the given project directory."""
    result = await save_creator_profile(profile_json, project_dir)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def vicin_save_creator_profile_raw(profile_json: str, project_dir: str) -> str:
    """Preview where the profile would be saved and its content — does not write any files."""
    return await save_creator_profile_raw(profile_json, project_dir)


# ── Workspace ─────────────────────────────────────────────────────────────────

@mcp.tool()
async def vicin_init_workspace(project_dir: str) -> str:
    """Set up the Vicin Studio folder structure in the given project directory."""
    result = await init_workspace(project_dir)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def vicin_init_workspace_raw(project_dir: str) -> str:
    """Preview the folder structure that would be created — does not write any files."""
    return await init_workspace_raw(project_dir)


# ── Project Guide ─────────────────────────────────────────────────────────────

@mcp.tool()
async def vicin_save_project_guide(content: str, project_dir: str) -> str:
    """Save a CLAUDE.md project guide to the given project directory."""
    result = await save_project_guide(content, project_dir)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def vicin_save_project_guide_raw(content: str, project_dir: str) -> str:
    """Preview where CLAUDE.md would be saved and its content — does not write any files."""
    return await save_project_guide_raw(content, project_dir)


# ── Script Writer ─────────────────────────────────────────────────────────────

@mcp.tool()
async def vicin_save_script(filename: str, content: str, project_dir: str) -> str:
    """Save a script to the scripts/ subfolder of the given project directory."""
    result = await save_script(filename, content, project_dir)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
async def vicin_save_script_raw(filename: str, content: str, project_dir: str) -> str:
    """Preview where a script would be saved and its content — does not write any files."""
    return await save_script_raw(filename, content, project_dir)


if __name__ == "__main__":
    mcp.run()
