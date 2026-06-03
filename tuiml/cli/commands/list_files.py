"""List Files Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('list-files')
@click.option('--builtin/--no-builtin', default=True, help='Include built-in tuiml algorithm files.')
@click.option('--user/--no-user', default=True, help='Include user-authored algorithm files.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def list_files(builtin, user, json_output):
    """List all algorithm source files — built-in and/or user-authored. Returns file paths, categories, and metadata. Use this before tuiml_read_algorithm to discover what's available and find the right name."""
    kwargs = {
            'builtin': builtin,
            'user': user,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_list_files', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
