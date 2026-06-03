"""Plot Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('plot')
@click.argument('plot_type')
@click.option('--model-id', type=str, help='Model ID from tuiml_train (required for most plot types)')
@click.option('--model-path', type=str, help='Path to saved model file (alternative to model_id)')
@click.option('--data', type=str, help='Data file path or built-in dataset name (required for confusion_matrix, roc_curve, pr_curve, learning_curve)')
@click.option('--target', type=str, help='Target column name (required for confusion_matrix, roc_curve, pr_curve, learning_curve)')
@click.option('--algorithm', type=str, help='Algorithm class name (required for learning_curve)')
@click.option('--title', type=str, help='Custom plot title (optional)')
@click.option('--normalize/--no-normalize', default=False, help='Normalize confusion matrix to show percentages (confusion_matrix only)')
@click.option('--experiment-results', type=str, help="Algorithm CV scores for comparison plots: { 'AlgoName': [score1, score2, ...], ... } (pass as JSON string)")
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def plot(plot_type, model_id, model_path, data, target, algorithm, title, normalize, experiment_results, json_output):
    """Generate a visualization/plot for model analysis. Returns the plot as an inline image. Supported plot types: confusion_matrix, roc_curve, pr_curve, learning_curve, tree, feature_importance."""
    kwargs = {
            'plot_type': plot_type,
            'model_id': model_id,
            'model_path': model_path,
            'data': data,
            'target': target,
            'algorithm': algorithm,
            'title': title,
            'normalize': normalize,
            'experiment_results': json.loads(experiment_results) if experiment_results is not None else None,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_plot', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
