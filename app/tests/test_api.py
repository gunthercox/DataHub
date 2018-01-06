import json
from unittest import TestCase
from datafeed.main import app, mongo


class ApiTestCase(TestCase):

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

        response_data = json.loads(response.data)

        # Remove the ids because we don't case what they are
        for item in response_data:
            del item['_id']

        self.assertEqual(response_data, [
            {'expires': None, 'name': 'Name 3', 'value': 3},
            {'expires': None, 'name': 'Name 2', 'value': 2},
            {'expires': None, 'name': 'Name 1', 'value': 1}
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

        self.assertEqual(response.status_code, 200, msg=response.data)

        response_data = json.loads(response.data)
        del response_data['_id']

        self.assertEqual(response_data, {
            'name': 'test',
            'value': 100,
            'expires': None
        })

        with app.app_context():
            events = mongo.db.events.find({'name': 'test', 'value': 100})

        self.assertEqual(events.count(), 1)

        event = events[0]
        self.assertEqual(event['expires'], None)

    def test_post_valid_event_with_expiration(self):
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

        with app.app_context():
            event_count = mongo.db.events.count()

        self.assertEqual(event_count, 0)

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

        with app.app_context():
            event_count = mongo.db.events.count()

        self.assertEqual(event_count, 0)
