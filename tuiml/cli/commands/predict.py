"""Predict Command - Make predictions using trained models via CLI."""

import click
import json
import numpy as np
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

@click.command('predict', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--model-path', help='Path to saved model file (alternative to --model-id)')
@click.option('--data', '-d', help='Path to data file or built-in dataset name')
@click.option('--model-id', help='Model ID returned by tuiml train')
@click.option('--steps', type=int, help='Number of forecast steps (timeseries only)')
@click.option('--output', '-o', help='Output file for predictions (CSV)')
@click.option('--stage', help="Atomic prediction stage: 'predict', 'predict_proba', 'forecast'")
@click.option('--json-output', is_flag=True, help='Output raw JSON')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
@click.pass_context
def predict(ctx, model_path, data, model_id, steps, output, stage, json_output, verbose):
    """Make predictions with a trained model or run a prediction stage.

    This command loads a previously saved model and uses it to generate 
    predictions or probabilities for a new dataset.
    """
    try:
        extra_kwargs = parse_extra_args(ctx.args)

        if verbose:
            click.echo("Running prediction workflow...")
            if stage:
                click.echo(f"  Stage: {stage}")
            if model_id:
                click.echo(f"  Model ID: {model_id}")
            if model_path:
                click.echo(f"  Model Path: {model_path}")
            if data:
                click.echo(f"  Data: {data}")
            if steps:
                click.echo(f"  Steps: {steps}")
            if extra_kwargs:
                click.echo(f"  Stage arguments: {extra_kwargs}")

        kwargs = {
            'model_id': model_id,
            'model_path': model_path,
            'data': data,
            'steps': steps,
            'output_path': output,
            'stage': stage,
            'stage_kwargs': extra_kwargs if extra_kwargs else None
        }
        kwargs = {k: v for k, v in kwargs.items() if v is not None}

        result = execute_tool('tuiml_predict', **kwargs)

        if result.get('status') == 'error':
            raise click.ClickException(result.get('error'))

        if json_output:
            click.echo(json.dumps(result, indent=2, default=str))
            return

        click.echo("\n" + "="*50)
        click.echo("Prediction Results")
        click.echo("="*50)

        if stage:
            click.echo(f"\nStage '{stage}' completed successfully.")

        if result.get('num_predictions') is not None:
            click.echo(f"\nNumber of predictions: {result.get('num_predictions')}")
        
        preview = result.get('predictions_preview')
        if preview is not None:
            click.echo(f"Predictions Preview: {preview}")

        if result.get('n_anomalies') is not None:
            click.echo(f"Normal instances: {result.get('n_normal')}")
            click.echo(f"Anomalies detected: {result.get('n_anomalies')}")
            click.echo(f"Anomaly ratio: {result.get('anomaly_ratio'):.4f}")

        if result.get('output_path'):
            click.echo(f"\nPredictions saved to: {result.get('output_path')}")

        click.echo("\n✓ Complete!")

    except Exception as e:
        if verbose:
            raise
        raise click.ClickException(str(e))
