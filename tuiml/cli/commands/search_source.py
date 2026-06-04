"""Search Source Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('search-source')
@click.option('--query', type=str, required=True, help='Regex pattern to search for.')
@click.option('--name', type=str, help='Scope search to one user algorithm by name. Omit to search all.')
@click.option('--builtin/--no-builtin', default=True, help='Search built-in algorithm files.')
@click.option('--user/--no-user', default=True, help='Search user-authored algorithm files.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def search_source(query, name, builtin, user, json_output):
    """Grep for a pattern inside algorithm source files. Returns matching lines with file path and line number — use this to locate a specific function, variable, or logic before editing. Accepts a regex pattern."""
    kwargs = {
            'query': query,
            'name': name,
            'builtin': builtin,
            'user': user,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_search_source', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
