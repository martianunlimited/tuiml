"""Upload Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('upload')
@click.option('--file-path', type=str, help='Path to an existing dataset file on disk. Supported: .csv, .tsv, .arff, .parquet, .pq, .xlsx, .xls, .json, .jsonl, .ndjson, .npy, .npz')
@click.option('--content', type=str, help="Raw text content for small inline datasets (use with 'format')")
@click.option('--format', type=str, help="File format — only needed with 'content'; auto-detected from file_path extension")
@click.option('--name', type=str, help='Optional name for the dataset (without extension)')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def upload(file_path, content, format, name, json_output):
    """Register a dataset for use with other TuiML tools. Provide either a file_path to an existing file on disk (preferred for large datasets), or content as raw text for small inline datasets. Supported formats: CSV, TSV, ARFF, Parquet, Excel (xlsx/xls), JSON, JSONL, NumPy (npy/npz). Returns a validated path for use with tuiml_train, tuiml_preprocess, etc."""
    kwargs = {
            'file_path': file_path,
            'content': content,
            'format': format,
            'name': name,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_upload_data', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
