"""Save Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('save')
@click.argument('model_id')
@click.argument('destination')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def save(model_id, destination, json_output):
    """Copy a trained model to a custom path. Use this when the user wants to save or download a model to a specific location."""
    kwargs = {
            'model_id': model_id,
            'destination': destination,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_save_model', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
