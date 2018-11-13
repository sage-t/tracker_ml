"""
  _                  _                       _
 | |                | |                     | |
 | |_ _ __ __ _  ___| | _____ _ __ _ __ ___ | |
 | __| '__/ _` |/ __| |/ / _ \ '__| '_ ` _ \| |
 | |_| | | (_| | (__|   <  __/ |_ | | | | | | |
  \__|_|  \__,_|\___|_|\_\___|_(_)|_| |_| |_|_|

Copyright 2018, tracker.ml
"""
import datetime
import json
import os
from collections import OrderedDict

import click


def _get_dir(ctx=None) -> str:
    """ Return path of .tracker/ directory """
    cd = os.getcwd()
    while True:
        tracker_dir = os.path.join(cd, ".tracker")
        if os.path.exists(tracker_dir):
            return tracker_dir
        else:
            new_cd = os.path.abspath(os.path.join(cd, os.pardir))
            if cd == new_cd:
                if ctx and ctx.obj.get("CLI", default=False):
                    click.secho("Error: tracker has not been initialized", fg="red")
                    exit(1)
                else:
                    raise FileNotFoundError(
                        "tracker has not been initialize. Use 'tracker init' in project root")
            else:
                cd = new_cd


def get_trials_dir(ctx=None) -> str:
    return os.path.join(_get_dir(ctx), "trials")


def get_config(ctx=None) -> dict:
    with open(os.path.join(_get_dir(ctx), "config.json"), "r") as fp:
        config = json.load(fp)
    return config


def set_config(config: dict, ctx=None):
    with open(os.path.join(_get_dir(ctx), "config.json"), "w+") as fp:
        json.dump(config, fp, indent=2)
    return config


def get_meta(trial="", ctx=None) -> dict:
    if trial:
        with open(os.path.join(get_trials_dir(ctx), trial, "meta.json"), "r") as fp:
            meta = json.load(fp, object_pairs_hook=OrderedDict)
        return meta
    else:
        with open(os.path.join(_get_dir(ctx), "meta.json"), "r") as fp:
            meta = json.load(fp, object_pairs_hook=OrderedDict)
        return meta


def set_meta(meta: dict, ctx=None):
    meta["updated"] = str(datetime.datetime.now())
    with open(os.path.join(_get_dir(ctx), "meta.json"), "w+") as fp:
        json.dump(meta, fp, indent=2)
    return meta


def get_trial_ids(ctx=None):
    return os.listdir(get_trials_dir(ctx))
