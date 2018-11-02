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
import hashlib
import os

import click

import tracker_ml.tools.file_ops as fo


def init_dir(api_key: str, rolling: bool, max_roll: int, ctx=None):
    if os.path.exists(".tracker/"):
        click.secho("Error: tracker was already initialized", fg="red")
        return

    os.makedirs(".tracker/")
    os.makedirs(".tracker/logs/")
    os.makedirs(".tracker/trials/")

    current_time = str(datetime.datetime.now())
    fo.set_meta({"created": current_time, "updated": current_time, "files": {}}, ctx)
    fo.set_config({"api_key": api_key, "rolling": rolling, "max_roll": max_roll}, ctx)


def __hash(data: str) -> str:
    return hashlib.md5(data.encode()).hexdigest()


def add_file(path: str, ctx=None):
    meta = fo.get_meta(ctx)

    if not os.path.exists(path):
        click.secho("Error: {} could not be located".format(path), fg="red")
        return
    elif os.path.isfile(path):
        if path not in meta["files"]:
            meta["files"][path] = __hash(path)
            click.echo("Added {}".format(path))
    else:
        for (dir_path, _, files) in os.walk(path):
            for f in files:
                p = os.path.join(dir_path, f)
                if p not in meta["files"]:
                    meta["files"][p] = __hash(p)
                    click.echo("Added {}".format(p))

    fo.set_meta(meta, ctx)


def remove_file(path: str, ctx=None):
    meta = fo.get_meta(ctx)

    if os.path.isfile(path):
        if path not in meta["files"]:
            click.secho("Error: {} is not tracked".format(path), fg="red")
            return

        meta["files"].pop(path)
    else:
        for (dir_path, _, files) in os.walk(path):
            for f in files:
                p = os.path.join(dir_path, f)
                if p in meta["files"]:
                    meta["files"].pop(p)

    fo.set_meta(meta, ctx)


def echo_status(sort_key: str, reverse: bool, limit: int, ctx=None):
    metas = [fo.get_meta(tid) for tid in fo.get_trial_ids()]

    click.echo(" Total trials: {}".format(len(metas)))

    if len(metas) == 0:
        return

    for meta in metas:
        for key in list(meta.keys()):
            if isinstance(meta[key], list):
                meta.pop(key)

    click.echo((" Reverse sorted" if reverse else " Sorted") + " by: {}".format(sort_key))
    metas.sort(key=lambda x: int(x[sort_key]), reverse=bool(not reverse))

    metas = [m for m in metas if list(m.keys()) == list(metas[0].keys())]

    if len(metas) > limit:
        click.echo(" Only displaying {} results".format(limit))
        metas = metas[:limit]

    max_len_values = dict([(k, len(k)) for k, _ in metas[0].items()])
    for meta in metas:
        for k, v in meta.items():
            if max_len_values[k] < len(str(v)):
                max_len_values[k] = len(str(v))

    data_str = []
    total_width = 1
    for key, max_len in max_len_values.items():
        width = max_len + 4
        total_width += width
        data_str.append("{:^" + str(width) + "}")

    click.echo("")
    click.echo("|".join(data_str).format(*[k.title() for k in max_len_values.keys()]))
    click.echo("-" * total_width)

    for meta in metas:
        click.echo("|".join(data_str).format(*list(meta.values())))
