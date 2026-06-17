"""Evaluate Command - Evaluate trained models on test data via CLI."""

import click
import json
from tuiml.agent.tools import execute_tool

def parse_extra_args(args):
    """Parse extra command-line arguments into a dictionary."""
    kwargs = {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith('--'):
            key = arg[2:]
        elif arg.startswith('-'):
            key = arg[1:]
        else:
            key = arg
            kwargs[key] = True
            i += 1
            continue

        if i + 1 < len(args) and not args[i+1].startswith('-'):
            val = args[i+1]
            if val.lower() == 'true':
                val = True
            elif val.lower() == 'false':
                val = False
            else:
                try:
                    val = int(val)
                except ValueError:
                    try:
                        val = float(val)
                    except ValueError:
                        pass
            kwargs[key] = val
            i += 2
        else:
            kwargs[key] = True
            i += 1
    return kwargs

@click.command('evaluate', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--model-path', help='Path to saved model file (alternative to --model-id)')
@click.option('--data', '-d', help='Path to data file or built-in dataset name')
@click.option('--target', '-t', help='Target column name')
@click.option('--model-id', help='Model ID returned by tuiml train')
@click.option('--metrics', '-m', multiple=True, help='Metrics to compute (default: auto)')
@click.option('--output', '-o', help='Output file for results (JSON)')
@click.option('--stage', help="Atomic evaluation stage: 'metrics', 'report'")
@click.option('--json-output', is_flag=True, help='Output raw JSON')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def evaluate(ctx, model_path, data, target, model_id, metrics, output, stage, json_output, verbose):
    """Evaluate a trained model on a test dataset or run an evaluation stage.

    This command computes performance metrics or generates descriptive reports
    for a model using a provided dataset.
    """
    try:
        extra_kwargs = parse_extra_args(ctx.args)

        if verbose:
            click.echo("Running evaluation workflow...")
            if stage:
                click.echo(f"  Stage: {stage}")
            if model_id:
                click.echo(f"  Model ID: {model_id}")
            if model_path:
                click.echo(f"  Model Path: {model_path}")
            if data:
                click.echo(f"  Data: {data}")
            if target:
                click.echo(f"  Target: {target}")
            if metrics:
                click.echo(f"  Metrics: {metrics}")
            if extra_kwargs:
                click.echo(f"  Stage arguments: {extra_kwargs}")

        metrics_list = list(metrics) if metrics else None

        kwargs = {
            'model_id': model_id,
            'model_path': model_path,
            'data': data,
            'target': target,
            'metrics': metrics_list,
            'stage': stage,
            'stage_kwargs': extra_kwargs if extra_kwargs else None
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        result = execute_tool('tuiml_evaluate', **kwargs)

        if result.get('status') == 'error':
            raise click.ClickException(result.get('error'))

        if json_output:
            click.echo(json.dumps(result, indent=2, default=str))
            return

        # Display results
        click.echo("\n" + "="*50)
        click.echo("Evaluation Results")
        click.echo("="*50)

        # Print report if report is available
        report = result.get('report')
        if report:
            click.echo(f"\n{report}")
        else:
            metrics_data = result.get('metrics')
            if metrics_data:
                click.echo()
                for metric_name, value in metrics_data.items():
                    if isinstance(value, float):
                        click.echo(f"  {metric_name:25s}: {value:.4f}")
                    else:
                        click.echo(f"  {metric_name:25s}: {value}")

        # Save results to file if requested
        if output:
            with open(output, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            click.echo(f"\nResults saved to: {output}")

        click.echo("\n✓ Complete!")

    except Exception as e:
        if verbose:
            raise
        raise click.ClickException(str(e))
