"""Test Statistics Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

@click.command('test-statistics')
@click.option('--test', type=str, required=True, help='Statistical test to run: - friedman: Non-parametric test for 3+ algorithms - nemenyi: Post-hoc pairwise test after Friedman - wilcoxon: Non-parametric pairwise test (2 algorithms) - paired_t: Parametric pairwise test (2 algorithms) - anova: Parametric test for 3+ groups - friedman_aligned: More powerful variant of Friedman - quade: Non-parametric test accounting for dataset difficulty')
@click.option('--results', type=str, required=True, help="Algorithm CV scores: { 'AlgorithmName': [score1, score2, ...], ... } (pass as JSON string)")
@click.option('--significance-level', type=float, help='Significance level (alpha), default 0.05')
@click.option('--higher-better/--no-higher-better', default=True, help='Whether higher scores are better (default True)')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
def test_statistics(test, results, significance_level, higher_better, json_output):
    """Run statistical significance tests on experiment results (cross-validation scores). Supports Friedman test, Nemenyi post-hoc, Wilcoxon signed-rank, paired t-test, one-way ANOVA, Friedman aligned ranks, and Quade test."""
    kwargs = {
            'test': test,
            'results': json.loads(results) if results else None,
            'significance_level': significance_level,
            'higher_better': higher_better,
    }
    # Remove None values
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    result = execute_tool('tuiml_test_statistics', **kwargs)
    if json_output:
        click.echo(json.dumps(result, indent=2, default=str))
    else:
        if result.get('status') == 'error':
            click.echo(f"Error: {result.get('error')}", err=True)
        else:
            # For now, print pretty JSON if not explicitly requested otherwise
            click.echo(json.dumps(result, indent=2, default=str))
