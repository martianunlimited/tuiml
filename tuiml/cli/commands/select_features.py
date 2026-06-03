"""Select Features Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('select-features')
@click.argument('data')
@click.argument('target')
@click.argument('method')
@click.option('--k', type=int, help='Number of top features to select (SelectKBestSelector)')
@click.option('--threshold', type=float, help='Threshold for VarianceThresholdSelector or SelectThresholdSelector')
@click.option('--method-params', type=str, help='Additional method-specific parameters (pass as JSON string)')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def select_features(data, target, method, k, threshold, method_params, json_output):
    """Run feature selection on a dataset and return selected feature names/indices. Supports filter methods (SelectKBestSelector, SelectPercentileSelector, VarianceThresholdSelector, SelectFprSelector, SelectThresholdSelector), correlation-based (CFSSelector), and wrapper methods (WrapperSelector)."""
    kwargs = {
            'data': data,
            'target': target,
            'method': method,
            'k': k,
            'threshold': threshold,
            'method_params': json.loads(method_params) if method_params is not None else None,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_select_features', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
