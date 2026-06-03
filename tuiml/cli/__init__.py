"""TuiML Command-Line Interface (CLI).

This package provides a comprehensive set of command-line tools for 
building, evaluating, and managing machine learning workflows.
"""

import click
from tuiml import __version__

@click.group()
@click.version_option(version=__version__, prog_name="tuiml")
@click.pass_context
def cli(ctx):
    """
    TuiML - Modern Machine Learning CLI

    A Python-based ML framework with three levels of API.
    Use exact class names everywhere - no mappings, fully scalable!
    """
    pass

# Import commands
from tuiml.cli.commands import (
    train, predict, evaluate, experiment, list_cmd,
    serve, setup, uninstall, info, update, mcp,
    status, trace, restart,
    upload, save, stop_server, plot, profile, generate,
    preprocess, select_features, test_statistics, tune,
    read_data, get_skeleton, create_algorithm, delete_algorithm,
    describe, read_algorithm, list_files, search_source, edit_algorithm
)

# Register commands
cli.add_command(train.train)
cli.add_command(predict.predict)
cli.add_command(evaluate.evaluate)
cli.add_command(experiment.experiment)
cli.add_command(list_cmd.list_algorithms)
cli.add_command(serve.serve)
cli.add_command(setup.setup)
cli.add_command(uninstall.uninstall)
cli.add_command(info.info)
cli.add_command(update.update)
cli.add_command(mcp.mcp)
cli.add_command(status.status)
cli.add_command(trace.trace)
cli.add_command(restart.restart)
cli.add_command(upload.upload)
cli.add_command(save.save)
cli.add_command(stop_server.stop_server)
cli.add_command(plot.plot)
cli.add_command(profile.profile)
cli.add_command(generate.generate)
cli.add_command(preprocess.preprocess)
cli.add_command(select_features.select_features)
cli.add_command(test_statistics.test_statistics)
cli.add_command(tune.tune)
cli.add_command(read_data.read_data)
cli.add_command(get_skeleton.get_skeleton)
cli.add_command(create_algorithm.create_algorithm)
cli.add_command(delete_algorithm.delete_algorithm)
cli.add_command(describe.describe)
cli.add_command(read_algorithm.read_algorithm)
cli.add_command(list_files.list_files)
cli.add_command(search_source.search_source)
cli.add_command(edit_algorithm.edit_algorithm)

def main():
    """Main entry point for CLI."""
    cli(obj={})

if __name__ == "__main__":
    main()
