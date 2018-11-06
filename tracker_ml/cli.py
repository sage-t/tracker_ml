#!/usr/bin/env python

"""
  _                  _                       _
 | |                | |                     | |
 | |_ _ __ __ _  ___| | _____ _ __ _ __ ___ | |
 | __| '__/ _` |/ __| |/ / _ \ '__| '_ ` _ \| |
 | |_| | | (_| | (__|   <  __/ |_ | | | | | | |
  \__|_|  \__,_|\___|_|\_\___|_(_)|_| |_| |_|_|

track.ml command line interface
"""
import os

import tracker_ml.tools as tools

__author__ = "Sage Thomas"
__copyright__ = "Copyright 2018, tracker.ml"
__version__ = "0.0.1"
__maintainer__ = "Sage Thomas"
__email__ = "sage.thomas@outlook.com"
__status__ = "Development"

import click


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)

    ctx.obj['CLI'] = True
    ctx.obj['DEBUG'] = debug


@cli.command()
@click.pass_context
@click.option("-k", "--api_key", default="", help="API key to bind to www.tracker.ml project")
@click.option("-r", "--roll", is_flag=True, help="Enable rolling trials")
@click.option("-m", "--max_roll", default=20, show_default=True, help="Max trials to save before rolling")
def init(ctx, api_key, roll, max_roll):
    """ Initializes tracker.ml project """
    tools.init_dir(api_key, roll, max_roll, ctx)


@cli.command()
@click.pass_context
@click.option("-k", "--sort_key", default="id", show_default=True, help="Key to sort by")
@click.option("-r", "--reverse", is_flag=True, help="Reverse the sort")
@click.option("-l", "--limit", default=10, show_default=True, help="Max amount of trials to display")
def status(ctx, sort_key, reverse, limit):
    """ List trials and recorded values """
    tools.echo_status(sort_key, reverse, limit, ctx)


@cli.command()
@click.pass_context
@click.argument("Trial_ID", type=click.INT)
def deploy(ctx, trial_id):
    """ Undo any file changes to revert tracked files to the given a trial's ID """
    tools.deploy_trial(trial_id, ctx)


# @cli.command()
# @click.pass_context
# def config(ctx):
#     """ Set any configuration options """


@cli.command()
@click.pass_context
@click.argument('path', type=click.Path(exists=True))
def add(ctx, path):
    """ Add a file or directory that will be tracked """
    tools.add_file(os.path.abspath(path), ctx)


@cli.command()
@click.pass_context
@click.argument('path', type=click.Path(exists=True))
def remove(ctx, path):
    """ Remove a file or directory that was being tracked """
    tools.remove_file(os.path.abspath(path), ctx)


# @cli.command()
# @click.pass_context
# def stash(ctx):
#     """ Stash given trials so they don't show up by default in the status command """


# @cli.command()
# @click.pass_context
# def tag(ctx):
#     """ Tag given trial so it can later be searched or sorted by the status command """


if __name__ == '__main__':
    cli(obj={})
