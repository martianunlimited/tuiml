"""Read Algorithm Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('read-algorithm')
@click.argument('name')
@click.option('--version', type=str, help="Specific version to read (e.g. '1.0.2'). Defaults to latest.")
@click.option('--builtin/--no-builtin', default=False, help='Set true to read a built-in tuiml algorithm instead of a user algorithm.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def read_algorithm(name, version, builtin, json_output):
    """Return the full source code of any algorithm — user-authored or built-in. For user algorithms pass the directory name (class name). For built-in algorithms set builtin=true and pass the class name (e.g. 'RandomForestClassifier') or file stem (e.g. 'random_forest'). Source is returned both raw and with line numbers for easy reference. Built-in algorithms are read-only; use tuiml_create_algorithm to fork them."""
    kwargs = {
            'name': name,
            'version': version,
            'builtin': builtin,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_read_algorithm', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
