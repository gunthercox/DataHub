import json
from unittest import TestCase
from datafeed.main import app, db


class ApiTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.endpoint = '/'

        # Clear the database before running the test
        db.flushall()

    def tearDown(self):
        db.flushall()

    def assertJSON(self, json_data, dict_data):
        """
        Assert that JSON data is equal to a dictionary of data.
        """
        import json
        from collections import OrderedDict

        data = json.loads(json_data)
        self.assertEqual(data, dict_data)

    def test_get_empty_list(self):
        response = self.app.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertJSON(response.data, [])

    def test_get_list(self):
        for i in range(1, 4):
            self.app.post(
                self.endpoint,
                data=json.dumps({
                    'name': 'Name %s' % i,
                    'value': i
                }),
                content_type='application/json'
            )

        response = self.app.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertJSON(response.data, [
            {'name': 'Name 3', 'value': 3},
            {'name': 'Name 2', 'value': 2},
            {'name': 'Name 1', 'value': 1}
        ])

    def test_post_valid_event(self):
        response = self.app.post(
            self.endpoint,
            data=json.dumps({
                'name': 'test',
                'value': 100
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200, str(response))
        self.assertJSON(response.data, {
            'name': 'test',
            'value': 100
        })

        self.assertEqual(len(db.keys()), 1)

        json_data = json.loads(response.data)

        self.assertIn('name', json_data)
        self.assertIn('value', json_data)
        self.assertEqual(json_data['name'], 'test')
        self.assertEqual(json_data['value'], 100)

        key = db.keys()[0]
        event = db.get(key)

        event_data = json.loads(event)

        self.assertEqual(event_data['name'], 'test')
        self.assertEqual(event_data['value'], 100)

    def test_post_valid_event_with_expiration(self):
        # TODO
        pass

    def test_post_event_without_name(self):
        response = self.app.post(
            self.endpoint,
            data=json.dumps({
                'value': 100
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSON(response.data, {
            'errors': [
                'The field "name" is required.'
            ]
        })

        self.assertEqual(len(db.keys()), 0)

    def test_post_event_without_value(self):
        response = self.app.post(
            self.endpoint,
            data=json.dumps({
                'name': 'test'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSON(response.data, {
            'errors': [
                'The field "value" is required.'
            ]
        })

        self.assertEqual(len(db.keys()), 0)
