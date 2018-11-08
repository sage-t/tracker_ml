"""
  _                  _                       _
 | |                | |                     | |
 | |_ _ __ __ _  ___| | _____ _ __ _ __ ___ | |
 | __| '__/ _` |/ __| |/ / _ \ '__| '_ ` _ \| |
 | |_| | | (_| | (__|   <  __/ |_ | | | | | | |
  \__|_|  \__,_|\___|_|\_\___|_(_)|_| |_| |_|_|

Copyright 2018, tracker.ml
"""
import atexit
import collections
import json
import logging
import os
from shutil import copyfile

import tracker_ml.file_ops as fo
from tracker_ml.api import TrackerMLAPI


class __TMLRun:
    """
    A Run is a single execution of a ml model train
    """

    def __init__(self):
        self.__trials_dir = fo.get_trials_dir()
        self.__id = max([int(f) for f in os.listdir(self.__trials_dir)], default=0) + 1
        self.__curr_dir = os.path.join(self.__trials_dir, str(self.__id))
        self.__meta = collections.OrderedDict()
        self.__meta["id"] = self.__id
        self.__api = None
        self.__model_name = ""

        atexit.register(self.__save)

    def login(self, username: str, password: str):
        self.__api = TrackerMLAPI(username, password)
        self.__api.ensure_token()

    def model(self, model_name: str):
        self.__model_name = model_name

    def record(self, key: str, value):
        if key in self.__meta:
            raise ValueError("{} already recorded".format(key))

        if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
            self.__meta[key] = value
        else:
            raise TypeError("Value must be of type str, int, or float")

    def mrecord(self, key: str, value):
        if key not in self.__meta:
            self.__meta[key] = []
        elif not isinstance(self.__meta[key], list):
            raise TypeError("Key was already used to record a single value")

        if isinstance(value, str) or isinstance(value, int) or isinstance(value, float):
            self.__meta[key].append(value)
        else:
            raise TypeError("Value must be of type str, int, or float")

    def __save(self):
        os.makedirs(self.__curr_dir)
        for file, md5 in fo.get_meta()["files"].items():
            copyfile(file, os.path.join(self.__curr_dir, md5))

        with open(os.path.join(self.__curr_dir, "meta.json"), "w+") as fp:
            json.dump(self.__meta, fp, indent=2)

        config = fo.get_config()
        meta = fo.get_meta()
        meta["current_trial"] = self.__id

        try:
            if self.__model_name and self.__api:
                meta["model_name"] = self.__model_name
                project_id = config["project_id"]

                if self.__model_name in meta["models"]:
                    model_id = meta["models"][self.__model_name]
                else:
                    model_id = self.__api.post_model(self.__model_name, project_id)
                    meta["models"][self.__model_name] = model_id

                self.__api.post_run(project_id, model_id, meta)
        except Exception as e:
            logging.exception("Problem using tracker.ml API")
        finally:
            fo.set_meta(meta)


__run = __TMLRun()


def login(username: str, password: str):
    """
    Set username and password to automatically upload run results to tracker.ml
    :param username: tracker.ml username
    :param password: tracker.ml password
    """
    __run.login(username, password)


def model(model_name: str):
    """
    Set the model for this run to by tied to. Creates model if it does not exist
    :param model_name: Name of model (ie "Logistic Regression")
    """
    __run.model(model_name)


def record(key: str, value):
    """
    Use to record a value relevant to the model
    :param key: String key that will be used to tag and compare with other models
    :param value: Value of type str, int, or float
    """
    __run.record(key, value)


def mrecord(key: str, value):
    """
    Use to record a series of values
    :param key: String key that will be used to tag data
    :param value: Value of type str, int, or float
    """
    __run.mrecord(key, value)