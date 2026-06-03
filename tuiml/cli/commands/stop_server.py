"""Stop Server Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('stop-server')
@click.option('--server-id', type=str, help='Server ID returned by tuiml_serve_model. If omitted, stops all servers.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def stop_server(server_id, json_output):
    """Stop a running model serving API server."""
    kwargs = {
            'server_id': server_id,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_stop_server', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
