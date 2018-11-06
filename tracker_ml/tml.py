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
import os
from shutil import copyfile

import tracker_ml.file_ops as fo


class __Trial:
    """
    A Trial is a single execution of a ml model train
    """

    def __init__(self):
        self.__trials_dir = fo.get_trials_dir()
        self.__id = max([int(f) for f in os.listdir(self.__trials_dir)], default=0) + 1
        self.__curr_dir = os.path.join(self.__trials_dir, str(self.__id))
        self.__meta = collections.OrderedDict()
        self.__meta["id"] = self.__id

        atexit.register(self.__save)

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

        meta = fo.get_meta()
        meta["current_trial"] = self.__id
        fo.set_meta(meta)


__trial = __Trial()


def record(key: str, value):
    """
    Use to record a value relevant to the model
    :param key: String key that will be used to tag and compare with other models
    :param value: Value of type str, int, or float
    """
    __trial.record(key, value)


def mrecord(key: str, value):
    """
    Use to record a series of values
    :param key: String key that will be used to tag data
    :param value: Value of type str, int, or float
    """
    __trial.mrecord(key, value)