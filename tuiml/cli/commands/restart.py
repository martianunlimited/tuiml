"""`tuiml restart` — kill every running tuiml-mcp; clients respawn it.

Most useful right after `tuiml update` to pick up the new code without
manually quitting each AI client.
"""
from __future__ import annotations

import json as _json

import click


@click.command()
@click.option("--json", "as_json", is_flag=True,
              help="Emit raw JSON instead of human-readable output.")
@click.option("--grace", type=float, default=2.0, show_default=True,
              help="Seconds to wait for SIGTERM before sending SIGKILL.")
def restart(as_json: bool, grace: float) -> None:
    """Restart every running tuiml-mcp process.

    Each AI client (Claude Desktop, Cursor, Codex, ...) automatically
    respawns its tuiml-mcp child when the previous one exits, so this
    is the right way to pick up a freshly installed version.
    """
    from tuiml.agent.restart_util import find_mcp_processes, kill_mcp_processes

    procs = find_mcp_processes(exclude_self=True)

    if as_json:
        result = kill_mcp_processes(procs=procs, grace_seconds=grace) if procs else {
            "killed": [], "failed": [], "self_exit_scheduled": False,
        }
        result["candidates"] = procs
        click.echo(_json.dumps(result, indent=2))
        return

    if not procs:
        click.echo("No tuiml-mcp processes running — nothing to restart.")
        click.echo("Open an AI client (Claude Desktop, Cursor, ...) to spawn one.")
        return

    click.echo(f"Restarting {len(procs)} tuiml-mcp instance(s):")
    for p in procs:
        click.echo(f"  pid {p['pid']:>6}  (parent pid {p['ppid']})")
    click.echo()

    result = kill_mcp_processes(procs=procs, grace_seconds=grace)

    if result["killed"]:
        click.echo(f"✓ Stopped: {', '.join(str(p) for p in result['killed'])}")
    if result["failed"]:
        for f in result["failed"]:
            click.echo(f"✗ pid {f['pid']}: {f['error']}", err=True)

    click.echo()
    click.echo("Your AI clients will respawn tuiml-mcp on the next request.")
