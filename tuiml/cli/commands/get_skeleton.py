"""Get Skeleton Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('get-skeleton')
@click.argument('kind')
@click.option('--class-name', type=str, help="Python identifier for the new class, e.g. 'MyGradientBoosting'.")
@click.option('--version', type=str, help="Initial semver, e.g. '1.0.0'.")
@click.option('--description', type=str, help='One-line docstring for the class.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def get_skeleton(kind, class_name, version, description, json_output):
    """Return a ready-to-edit Python source template for a new @classifier or @regressor class. Agents should call this, fill in fit() and predict(), then pass the completed source to tuiml_create_algorithm. Feature-gated: requires env TUIML_ALLOW_USER_ALGORITHMS=1."""
    kwargs = {
            'kind': kind,
            'class_name': class_name,
            'version': version,
            'description': description,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_get_skeleton', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
