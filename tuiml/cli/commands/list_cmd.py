"""List Command - Browse available algorithms in the registry via CLI."""

import click
import tuiml

DESC_MAX_LEN = 60

@click.command('list')
@click.option('--category', '-c', type=click.Choice(['algorithm', 'preprocessing', 'dataset', 'feature', 'splitting', 'custom', 'all']),
              default='all', help='Category to list (default: all)')
@click.option('--type', '-t', type=click.Choice(['classifier', 'regressor', 'clusterer', 'anomaly', 'timeseries', 'all']),
              default='all', help='Filter by algorithm type (default: all)')
@click.option('--search', '-s', help='Search query for filtering')
@click.option('--include-runs', is_flag=True, help='Include run history for custom algorithms')
@click.option('--limit', type=int, default=50, help='Maximum number of results to return')
@click.option('--offset', type=int, default=0, help='Number of results to skip')
@click.option('--format', '-f', type=click.Choice(['table', 'json', 'names']),
              default='table', help='Output format (default: table)')
@click.option('--verbose', '-v', is_flag=True, help='Show detailed information')
def list_algorithms(category, type, search, include_runs, limit, offset, format, verbose):
    """Browse and search for available components in the registry.

    This command lists registered components (algorithms, datasets, preprocessing),
    allowing you to filter by category, type, or search keywords.

    Parameters
    ----------
    category : {"algorithm", "preprocessing", "dataset", "feature", "splitting", "custom", "all"}
        Filter by component category.
    type : {"classifier", "regressor", "clusterer", "anomaly", "timeseries", "all"}
        Filter by algorithm type.
    search : str, optional
        A search query to filter by name or description.
    include_runs : bool
        Include run history for custom algorithms.
    limit : int
        Maximum results to return.
    offset : int
        Number of results to skip.
    format : {"table", "json", "names"}, default="table"
        The desired output format.
    verbose : bool, default=False
        Whether to show detailed metadata.
    """
    try:
        from tuiml.agent.tools import execute_tool
        
        kwargs = {
            'category': category,
            'limit': limit,
            'offset': offset,
            'include_runs': include_runs
        }
        if search:
            kwargs['search'] = search
        if type != 'all':
            kwargs['type'] = type
            
        result = execute_tool('tuiml_list', **kwargs)
        
        if result.get('status') == 'error':
            raise click.ClickException(result.get('error', 'Unknown error'))
            
        components = result.get('components', result.get('algorithms', []))
        
        if not components:
            click.echo("No components found.")
            return

        # Display based on format
        if format == 'names':
            for comp in components:
                click.echo(comp.get('name', 'Unknown'))

        elif format == 'json':
            import json
            click.echo(json.dumps(result, indent=2))

        else:  # table format
            click.echo("\n" + "="*80)
            click.echo(f"Available Components (Total: {result.get('total', len(components))})")
            click.echo("="*80)
            click.echo()

            # Group by category
            grouped = {}
            for comp in components:
                comp_cat = comp.get('category', 'unknown')
                if comp_cat not in grouped:
                    grouped[comp_cat] = []
                grouped[comp_cat].append(comp)

            for comp_cat, comps in sorted(grouped.items()):
                click.echo(f"\n{comp_cat.upper()}S:")
                click.echo("-" * 80)
                for comp in sorted(comps, key=lambda x: x.get('name', '')):
                    name = comp.get('name', 'Unknown')
                    desc = comp.get('description', 'No description')
                    
                    if verbose:
                        click.echo(f"\n  {name}")
                        click.echo(f"    {desc}")
                        if 'tags' in comp:
                            click.echo(f"    Tags: {', '.join(comp['tags'])}")
                        if 'type' in comp and comp['type'] != comp_cat:
                            click.echo(f"    Type: {comp['type']}")
                    else:
                        desc_short = desc[:DESC_MAX_LEN] + "..." if len(desc) > DESC_MAX_LEN else desc
                        click.echo(f"  {name:30s} - {desc_short}")

            click.echo(f"\nShowing {len(components)} of {result.get('total', len(components))} items")
            if result.get('has_more'):
                click.echo(f"Use --offset {offset + limit} to see more")
            click.echo()

    except Exception as e:
        if verbose:
            raise
        raise click.ClickException(str(e))
