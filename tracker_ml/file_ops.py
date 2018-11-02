"""
  _                  _                       _
 | |                | |                     | |
 | |_ _ __ __ _  ___| | _____ _ __ _ __ ___ | |
 | __| '__/ _` |/ __| |/ / _ \ '__| '_ ` _ \| |
 | |_| | | (_| | (__|   <  __/ |_ | | | | | | |
  \__|_|  \__,_|\___|_|\_\___|_(_)|_| |_| |_|_|

Copyright 2018, tracker.ml
"""
import json
import os


def get_dir() -> str:
    """ Return path of .tracker/ directory """
    cd = os.getcwd()
    while True:
        tracker_dir = os.path.join(cd, ".tracker")
        if os.path.exists(tracker_dir):
            return tracker_dir
        else:
            new_cd = os.path.abspath(os.path.join(cd, os.pardir))
            if cd == new_cd:
                raise FileNotFoundError(
                    "tracker has not been initialize. Use 'tracker init' in project root")
            else:
                cd = new_cd


def get_trials_dir() -> str:
    return os.path.join(get_dir(), "trials")


def get_config() -> dict:
    with open(os.path.join(get_dir(), "config.json"), "r") as fp:
        config = json.load(fp)
    return config


def get_meta() -> dict:
    with open(os.path.join(get_dir(), "meta.json"), "r") as fp:
        meta = json.load(fp)
    return meta
