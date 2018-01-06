import json
from tests.testcases import AppTestCase
from datafeed.main import app, mongo


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

        response_data = json.loads(response.data)
        del response_data['_id']

        self.assertEqual(response_data, {
            'name': 'test',
            'value': 100,
            'expires': None
        })

        with app.app_context():
            events = mongo.db.events.find({'name': 'test'})

        self.assertEqual(events.count(), 1)

        event = events[0]
        self.assertEqual(event['name'], 'test')
        self.assertEqual(event['value'], 100)
        self.assertEqual(event['expires'], None)

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

        response_data = json.loads(response.data)
        del response_data['_id']

        self.assertEqual(response_data, {
            'name': 'test',
            'value': 200,
            'expires': 30
        })

        with app.app_context():
            events = mongo.db.events.find({'name': 'test'})

        self.assertEqual(events.count(), 1)

        event = events[0]
        self.assertEqual(event['name'], 'test')
        self.assertEqual(event['value'], 200)
        self.assertEqual(event['expires'], 30)

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
