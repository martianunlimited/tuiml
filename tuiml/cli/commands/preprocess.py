"""Preprocess Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('preprocess')
@click.option('--data', type=str, required=True, help='Data file path or built-in dataset name')
@click.option('--target', type=str, help='Target column name (excluded from preprocessing, re-appended to output)')
@click.option('--steps', type=str, required=True, help="Preprocessing steps as names or objects with params. Examples: ['StandardScaler', 'SimpleImputer'] or [{'name': 'SimpleImputer', 'strategy': 'median'}, 'MinMaxScaler'] (pass as JSON string)")
@click.option('--save-as', type=str, help='Custom output file path (optional, defaults to temp file)')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def preprocess(data, target, steps, save_as, json_output):
    """Apply preprocessing steps to a dataset and return the result as a new file. Supports any registered preprocessor (e.g., StandardScaler, MinMaxScaler, SimpleImputer, PCA). Steps can be strings or objects with parameters."""
    kwargs = {
            'data': data,
            'target': target,
            'steps': json.loads(steps) if steps else None,
            'save_as': save_as,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_preprocess', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
