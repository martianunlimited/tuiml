"""Edit Algorithm Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('edit-algorithm')
@click.argument('name')
@click.argument('old_string')
@click.argument('new_string')
@click.option('--version', type=str, help='Target a specific version. Defaults to latest.')
@click.option('--bump-version/--no-bump-version', default=False, help='Save the edit as a new patch version instead of overwriting the current one.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def edit_algorithm(name, old_string, new_string, version, bump_version, json_output):
    """Apply a targeted str_replace edit to a user algorithm. Replaces exactly one occurrence of old_string with new_string — fails loudly if old_string is not found or appears more than once (make it more specific with surrounding context). The edited source is AST-validated and the algorithm is re-registered so all MCP tools immediately see the change. Workflow: tuiml_read_algorithm → identify the text to change → tuiml_edit_algorithm. Set bump_version=true to save as a new patch version instead of overwriting. Built-in algorithms cannot be edited — fork them first with tuiml_create_algorithm. Feature-gated: requires env TUIML_ALLOW_USER_ALGORITHMS=1."""
    kwargs = {
            'name': name,
            'old_string': old_string,
            'new_string': new_string,
            'version': version,
            'bump_version': bump_version,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_edit_algorithm', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
