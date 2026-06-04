"""Read Data Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('read-data')
@click.option('--data', type=str, required=True, help="Data file path or built-in dataset name (e.g., 'iris', '/tmp/tuiml_preprocessed/file.csv')")
@click.option('--n-rows', type=int, help='Number of rows to return (default: 10, max: 100)')
@click.option('--mode', type=str, help="How to select rows: - head: First n_rows (default) - tail: Last n_rows - sample: Random sample of n_rows - indices: Specific row indices (provide 'indices' parameter)")
@click.option('--indices', type=str, help="Specific row indices to return (only used when mode='indices') (pass as JSON string)")
@click.option('--columns', type=str, help='Subset of columns to return (optional, returns all if omitted) (pass as JSON string)')
@click.option('--include-target/--no-include-target', default=True, help='Include the target column in the output (default: True)')
@click.option('--target', type=str, help='Target column name (used to label the target in the output)')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def read_data(data, n_rows, mode, indices, columns, include_target, target, json_output):
    """Read and preview actual rows from a dataset. Returns sample rows as a list of dictionaries. Supports head, tail, random sample, or specific row indices."""
    kwargs = {
            'data': data,
            'n_rows': n_rows,
            'mode': mode,
            'indices': json.loads(indices) if indices is not None else None,
            'columns': json.loads(columns) if columns is not None else None,
            'include_target': include_target,
            'target': target,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_read_data', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
