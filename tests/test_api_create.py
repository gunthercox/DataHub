import json
from tests.testcases import AppTestCase
from datahub.main import redis


class ApiCreateTestCase(AppTestCase):

    def test_post_valid_event(self):
        response = self.app.post(
            self.endpoint,
            data=json.dumps({
                'name': 'test',
                'value': 100
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200, msg=response.data)

        self.assertEqual(response.json, {
            'name': 'test',
            'value': 100,
            'expires': None
        })

        event_value = redis.get('test')

        self.assertIsNotNone(event_value)
        self.assertEqual(int(event_value), 100)

    def test_post_valid_event_with_expiration(self):
        response = self.app.post(
            self.endpoint,
            data=json.dumps({
                'name': 'test',
                'value': 200,
                'expires': 30
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200, msg=response.data)

        self.assertEqual(response.json, {
            'name': 'test',
            'value': 200,
            'expires': 30
        })

        event_value = redis.get('test')

        self.assertIsNotNone(event_value)
        self.assertEqual(int(event_value), 200)

    def test_post_event_without_name(self):
        response = self.app.post(
            self.endpoint,
            data=json.dumps({
                'value': 100
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            'errors': [
                'The field "name" is required.'
            ]
        })

        keys = redis.keys()

        self.assertEqual(len(keys), 0)

    def test_post_event_without_value(self):
        response = self.app.post(
            self.endpoint,
            data=json.dumps({
                'name': 'test'
            }),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            'errors': [
                'The field "value" is required.'
            ]
        })

        keys = redis.keys()

        self.assertEqual(len(keys), 0)
