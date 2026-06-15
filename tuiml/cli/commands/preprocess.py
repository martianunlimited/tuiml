"""Preprocess Command - Auto-generated from MCP schema."""

import click
import json
from tuiml.agent.tools import execute_tool

def parse_extra_args(args):
    """Parse extra command-line arguments into a dictionary.
    
    Examples:
        ['--kfold', '10', '--strategy', 'mean', '--cv'] -> {'kfold': 10, 'strategy': 'mean', 'cv': True}
    """
    kwargs = {}
    i = 0
    while i < len(args):
        arg = args[i]
        if arg.startswith('--'):
            key = arg[2:]
        elif arg.startswith('-'):
            key = arg[1:]
        else:
            # Treating positional argument/malformed as flag key
            key = arg
            kwargs[key] = True
            i += 1
            continue

        # Check if next arg is the value
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

@click.command('preprocess', context_settings=dict(
    ignore_unknown_options=True,
    allow_extra_args=True,
))
@click.option('--data', type=str, required=True, help='Data file path or built-in dataset name')
@click.option('--target', type=str, help='Target column name (excluded from preprocessing, re-appended to output)')
@click.option('--steps', type=str, help="Preprocessing steps as names or objects with params. Examples: ['StandardScaler', 'SimpleImputer'] (pass as JSON string)")
@click.option('--stage', type=str, help="Atomic preprocessing stage to execute: 'split', 'impute', 'balance', 'scale', 'encode', 'discretize'")
@click.option('--output', type=str, help="Output path to save the generated file(s)")
@click.option('--save-as', type=str, help='Custom output file path (optional, alias for output)')
@click.option('--json-output', is_flag=True, help='Output raw JSON')
@click.pass_context
def preprocess(ctx, data, target, steps, stage, output, save_as, json_output):
    """Apply preprocessing steps or a specific atomic stage to a dataset.
    
    Supports running standard pipelines or single atomic stages like split, impute,
    balance, scale, encode, and discretize. Additional stage-specific arguments
    (e.g., --kfold 10) can be passed directly.
    """
    extra_kwargs = parse_extra_args(ctx.args)
    
    kwargs = {
            'data': data,
            'target': target,
            'steps': json.loads(steps) if steps else None,
            'stage': stage,
            'output': output or save_as,
            'stage_kwargs': extra_kwargs if extra_kwargs else None,
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
            click.echo(json.dumps(result, indent=2, default=str))
