from unittest import TestCase
from datafeed.main import app, mongo


class AppTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.endpoint = '/'

    def tearDown(self):
        with app.app_context():
            mongo.db.events.drop()

    def assertJSON(self, json_data, dict_data):
        """
        Assert that JSON data is equal to a dictionary of data.
        """
        import json

        data = json.loads(json_data)
        self.assertEqual(data, dict_data)
