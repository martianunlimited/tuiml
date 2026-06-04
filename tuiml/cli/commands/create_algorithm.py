"""Create Algorithm Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('create-algorithm')
@click.option('--name', type=str, required=True, help='Directory name — usually equal to the class name (Python identifier).')
@click.option('--kind', type=str, required=True, help="Task kind. Must match the imported class's base type.")
@click.option('--code', type=str, required=True, help='Full Python source. Must define exactly one @classifier or @regressor class.')
@click.option('--version', type=str, help="Semver for this submission, e.g. '1.0.0', '1.0.1'.")
@click.option('--description', type=str, help='Optional short description (falls back to the class docstring).')
@click.option('--force/--no-force', default=False, help='Overwrite an existing file at <name>/<version>/. Bump the version instead when possible.')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def create_algorithm(name, kind, code, version, description, force, json_output):
    """Persist, validate, and register a new agent-authored algorithm. The source is AST-validated (forbidden modules: subprocess, socket, os, urllib, requests, …; forbidden calls: eval, exec, open, __import__) and saved to ~/.tuiml/user_algorithms/<name>/<version>/algorithm.py. After registration, the algorithm is available via its class name to every existing MCP tool (tuiml_train, tuiml_experiment, tuiml_describe). Each version is also registered under a pinned alias <ClassName>_v<major>_<minor>_<patch> so you can A/B compare versions inside a single tuiml_experiment. Feature-gated: requires env TUIML_ALLOW_USER_ALGORITHMS=1."""
    kwargs = {
            'name': name,
            'kind': kind,
            'code': code,
            'version': version,
            'description': description,
            'force': force,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_create_algorithm', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
