"""Profile Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('profile')
@click.option('--data', type=str, required=True, help="Data file path or built-in dataset name (e.g., 'iris', 'wine', '/path/to/data.csv')")
@click.option('--target', type=str, help='Target column name (optional, used for class distribution)')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def profile(data, target, json_output):
    """Inspect a dataset before training — shape, dtypes, missing values, basic statistics, and class distribution. Works with file paths or built-in dataset names."""
    kwargs = {
            'data': data,
            'target': target,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_profile_data', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
