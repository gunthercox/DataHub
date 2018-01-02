import json
from unittest import TestCase
from datafeed.main import app, db, Event


class ApiTestCase(TestCase):

    def setUp(self):

        # Use an in-memory database for testing
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'

        self.app = app.test_client()

        self.endpoint = '/'

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

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
            event = Event(
                name='Name %s' % i,
                value=i
            )
            db.session.add(event)
        db.session.commit()

        response = self.app.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertJSON(response.data, [
            {'expires': None, 'id': 3, 'name': 'Name 3', 'value': '3'},
            {'expires': None, 'id': 2, 'name': 'Name 2', 'value': '2'},
            {'expires': None, 'id': 1, 'name': 'Name 1', 'value': '1'}
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

        self.assertEqual(response.status_code, 200)
        self.assertJSON(response.data, {
            'id': 1,
            'name': 'test',
            'value': '100',
            'expires': None
        })

        events = Event.query.filter_by(name='test', value=100)
        self.assertEqual(events.count(), 1)

        event = events.first()
        self.assertEqual(event.expires, None)

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

        self.assertEqual(Event.query.count(), 0)

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

        self.assertEqual(Event.query.count(), 0)
