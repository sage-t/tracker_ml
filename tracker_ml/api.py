"""
  _                  _                       _
 | |                | |                     | |
 | |_ _ __ __ _  ___| | _____ _ __ _ __ ___ | |
 | __| '__/ _` |/ __| |/ / _ \ '__| '_ ` _ \| |
 | |_| | | (_| | (__|   <  __/ |_ | | | | | | |
  \__|_|  \__,_|\___|_|\_\___|_(_)|_| |_| |_|_|

Currently still in development.

Copyright 2018, tracker.ml
"""
import json
import time

import requests


class TrackerMLAPI:

    def __init__(self, username: str, password: str, base_url="http://127.0.0.1:9000"):
        self.__base_url = base_url
        self.__username = username
        self.__password = password
        self.__token = ""
        self.__expiration = 0

    def _format_url(self, path: str) -> str:
        return "{}/{}".format(self.__base_url, path)

    def _format_headers(self, headers=None) -> dict:
        self.ensure_token()

        token_header = {"token": self.__token}

        if isinstance(headers, dict):
            headers.update(token_header)
        elif headers is None:
            headers = token_header
        else:
            raise TypeError("headers must be a dict or None")

        return headers

    def ensure_token(self):
        if self.__token and int(time.time()) < self.__expiration:
            return

        url = self._format_url("login?")
        body = json.dumps({"username": self.__username, "password": self.__password})

        r = requests.post(url, data=body)

        data = r.json()
        self.__token = data["jwt"]
        self.__expiration = int(data["expiration"])

    def post_project(self, project_name: str) -> dict:
        url = self._format_url("project")
        body = json.dumps({"Name": project_name})
        headers = self._format_headers()

        r = requests.post(url, data=body, headers=headers)

        return r.json()

    def get_projects(self) -> list:
        url = self._format_url("project")
        headers = self._format_headers()

        r = requests.get(url, headers=headers)

        return r.json()

    def post_model(self, name: str, project_id: int) -> str:
        url = self._format_url("model")
        body = json.dumps({"type": name, "project_id": project_id})
        headers = self._format_headers()

        r = requests.post(url, data=body, headers=headers)

        return str(r.text)

    def post_run(self, project_id: int, model_id: str, parameters: dict):
        url = self._format_url("runs")
        body = json.dumps({"model_id": model_id, "project_id": project_id, "parameters": parameters})
        headers = self._format_headers()

        r = requests.post(url, data=body, headers=headers)

    def get_runs(self, project_id: int, model_id: str):
        url = self._format_url("runs?project_id={}&model_id={}".format(project_id, model_id))
        headers = self._format_headers()

        r = requests.post(url, headers=headers)

        raise NotImplementedError()