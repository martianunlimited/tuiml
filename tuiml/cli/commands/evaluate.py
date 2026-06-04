"""Evaluate Command - Evaluate trained models on test data via CLI."""

import click
import tuiml

@click.command()
@click.option('--model-path', help='Path to saved model file (alternative to --model-id)', type=click.Path(exists=True))
@click.option('--data', '-d', help='Path to data file or built-in dataset name')
@click.option('--target', '-t', help='Target column name')
@click.option('--model-id', help='Model ID returned by tuiml train')
@click.option('--metrics', '-m', multiple=True, help='Metrics to compute (default: auto)')
@click.option('--output', '-o', help='Output file for results (JSON)')
@click.option('--verbose', '-v', is_flag=True, help='Verbose output')
def evaluate(model_path, data, target, model_id, metrics, output, verbose):
    """Evaluate a trained model on a test dataset.

    This command computes performance metrics for a model using a provided 
    labeled test dataset.

    Parameters
    ----------
    model_path : str
        Path to the saved model file (e.g., ``"model.pkl"``).
    data : str
        Path to the test data file (CSV, ARFF, etc.).
    target : str
        Name of the target column in the dataset.
    metrics : list of str, optional
        A list of metric names to compute. If not provided, metrics are 
        automatically selected based on the task type.
    output : str, optional
        Path to save the evaluation results as a JSON file.
    verbose : bool, default=False
        Whether to enable verbose output.

    Examples
    --------
    Evaluate with auto-detected metrics:

    >>> tuiml evaluate model.pkl test.csv class

    Evaluate with specific performance metrics:

    >>> tuiml evaluate model.pkl test.csv label -m accuracy -m f1 -m precision

    Save the evaluation results to a JSON file:

    >>> tuiml evaluate model.pkl test.csv class -o results.json
    """
    try:
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

        if verbose:
            click.echo(f"Loading data from: {data}")

        # Load data
        from tuiml.datasets import load
        dataset = load(data)
        X = dataset.X
        y = dataset.get_target(target)

        if verbose:
            click.echo(f"Evaluating on {len(X)} samples...")

        # Build metrics list
        metrics_list = list(metrics) if metrics else "auto"

        # Evaluate
        results = tuiml.evaluate(model, X, y, metrics=metrics_list)

        # Display results
        click.echo("\n" + "="*50)
        click.echo("Evaluation Results")
        click.echo("="*50)
        click.echo()

        for metric_name, value in results.items():
            click.echo(f"  {metric_name:20s}: {value:.4f}")

        # Save results to file if requested
        if output:
            import json
            with open(output, 'w') as f:
                json.dump(results, f, indent=2)
            click.echo(f"\nResults saved to: {output}")

        click.echo("\n✓ Evaluation complete!")

    except Exception as e:
        if verbose:
            raise
        raise click.ClickException(str(e))
