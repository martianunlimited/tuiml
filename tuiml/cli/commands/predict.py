"""Predict Command - Make predictions using trained models via CLI."""

import click
import tuiml

@click.command()
@click.argument('model_path', required=False, type=click.Path(exists=True))
@click.argument('data', required=False, type=click.Path(exists=True))
@click.option('--model-id', help='Model ID returned by tuiml train')
@click.option('--steps', type=int, help='Number of forecast steps (timeseries only)')
@click.option('--output', '-o', help='Output file for predictions (CSV)')
@click.option('--format', '-f', type=click.Choice(['csv', 'json', 'npy']), default='csv',
              help='Output format (default: csv)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def predict(model_path, data, model_id, steps, output, format, verbose):
    """Make predictions with a trained model.

    This command loads a previously saved model and uses it to generate 
    predictions for a new dataset.

    Parameters
    ----------
    model_path : str
        Path to the saved model file (e.g., ``"model.pkl"``).
    data : str
        Path to the data file for making predictions.
    output : str, optional
        Path where the predictions should be saved.
    format : {"csv", "json", "npy"}, default="csv"
        Format for the output predictions file.
    verbose : bool, default=False
        Whether to enable verbose output.

    Examples
    --------
    Predict and save results to a CSV file:

    >>> tuiml predict model.pkl test_data.csv -o predictions.csv

    Predict and save as a NumPy array:

    >>> tuiml predict model.pkl test_data.csv -o predictions.npy -f npy
    """
    try:
        import numpy as np
        import pandas as pd
        from tuiml.agent.tools import _load_model_from_disk

        if not model_path and not model_id:
            raise click.UsageError("Must provide either MODEL_PATH argument or --model-id option.")

        if model_id:
            if verbose:
                click.echo(f"Loading model from ID: {model_id}")
            model = _load_model_from_disk(model_id=model_id)
            if not model:
                raise click.ClickException(f"Model ID '{model_id}' not found.")
        else:
            if verbose:
                click.echo(f"Loading model from: {model_path}")
            model = tuiml.load(model_path)

        if not data and not steps:
             raise click.UsageError("Must provide DATA argument or --steps option (for timeseries).")

        if data:
            if verbose:
                click.echo(f"Loading data from: {data}")
            from tuiml.datasets import load
            dataset = load(data)
            X = dataset.X

            if verbose:
                click.echo(f"Making predictions on {len(X)} samples...")
            predictions = tuiml.predict(model, X)
        else:
            if verbose:
                click.echo(f"Making predictions for {steps} steps...")
            predictions = model.predict(steps)

        # Display summary
        click.echo("\n" + "="*50)
        click.echo("Prediction Results")
        click.echo("="*50)
        click.echo(f"\nPredicted {len(predictions)} samples")
        click.echo(f"Unique values: {len(np.unique(predictions))}")

        # Save predictions
        if output:
            if format == 'csv':
                df = pd.DataFrame({'prediction': predictions})
                df.to_csv(output, index=False)
            elif format == 'json':
                import json
                with open(output, 'w') as f:
                    json.dump(predictions.tolist(), f)
            elif format == 'npy':
                np.save(output, predictions)

            click.echo(f"\nPredictions saved to: {output}")
        else:
            # Print first 10 predictions
            click.echo(f"\nFirst 10 predictions: {predictions[:10]}")

        click.echo("\n✓ Prediction complete!")

    except Exception as e:
        if verbose:
            raise
        raise click.ClickException(str(e))
