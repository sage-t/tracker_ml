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
import random
import string
import unittest

from requests import HTTPError

from tracker_ml.api import TrackerMLAPI


class TrackerMLAPITest(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:9000"

    @staticmethod
    def _random_str():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def test_signup_and_login(self):
        username = self._random_str()
        password = self._random_str()

        api = TrackerMLAPI(username, password, base_url=self.BASE_URL)
        api.create_user()
        api.ensure_token()

        self.assertTrue(bool(api._token))
        self.assertGreater(api._expiration, 0)

        with self.assertRaises(HTTPError):
            api.create_user()

    def test_projects(self):
        username = self._random_str()
        password = self._random_str()
        project_name = self._random_str()

        api = TrackerMLAPI(username, password, base_url=self.BASE_URL)
        api.create_user()

        self.assertEqual(len(api.get_projects()), 0)
        project = api.post_project(project_name)
        self.assertEqual(project["name"], project_name)

        projects = api.get_projects()
        self.assertEqual(len(projects), 1)
        self.assertEqual(project["name"], projects[0]["name"])
        self.assertEqual(project["id"], projects[0]["id"])
        self.assertEqual(project["creator_id"], projects[0]["creator_id"])

        with self.assertRaises(HTTPError):
            api.post_project(project_name)

    def test_models(self):
        username = self._random_str()
        password = self._random_str()
        project_name = self._random_str()
        model_name = self._random_str()

        api = TrackerMLAPI(username, password, base_url=self.BASE_URL)
        api.create_user()

        project_id = api.post_project(project_name)["id"]
        self.assertEqual(len(api.get_models(project_id)), 0)

        model_id = api.post_model(model_name, project_id)
        models = api.get_models(project_id)

        self.assertEqual(len(models), 1)
        self.assertEqual(model_name, models[0]["type"])
        self.assertEqual(model_id, models[0]["model_id"])
        self.assertEqual(project_id, models[0]["project_id"])

        with self.assertRaises(HTTPError):
            api.post_model(model_name, project_id)

    def test_runs(self):
        username = self._random_str()
        password = self._random_str()
        project_name = self._random_str()
        model_name = self._random_str()

        api = TrackerMLAPI(username, password, base_url=self.BASE_URL)
        api.create_user()
        project_id = api.post_project(project_name)["id"]
        model_id = api.post_model(model_name, project_id)

        self.assertEqual(len(api.get_runs(project_id, model_id)), 0)

        params = {"p1": 1}
        api.post_run(project_id, model_id, params)
        runs = api.get_runs(project_id, model_id)
        self.assertEqual(len(runs), 1)
        self.assertEqual(runs[0]["parameters"], params)
