"""Delete Algorithm Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('delete-algorithm')
@click.argument('name')
@click.option('--version', type=str, help='If omitted, all versions are removed.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def delete_algorithm(name, version, json_output):
    """Delete a user algorithm from disk. Pass only `name` to remove every version; pass both to remove a single version. Registry entries for already-loaded classes remain until the MCP server restarts. Feature-gated: requires env TUIML_ALLOW_USER_ALGORITHMS=1."""
    kwargs = {
            'name': name,
            'version': version,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_delete_algorithm', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
