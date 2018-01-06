import json
from tests.testcases import AppTestCase
from datafeed.main import app, mongo


class ApiDeleteTestCase(AppTestCase):

    def test_delete_expired_event(self):
        """
        Test that any expired events are deleted.
        """

        self.app.post(
            self.endpoint,
            data=json.dumps({
                'name': 'not expired',
                'value': 100,
                'expires': 60
            }),
            content_type='application/json'
        )

        self.app.post(
            self.endpoint,
            data=json.dumps({
                'name': 'expired',
                'value': 100,
                'expires': -60
            }),
            content_type='application/json'
        )

        # Test that the events exist before the delete request

        with app.app_context():
            count = mongo.db.events.count()

        self.assertEqual(count, 2)

        self.app.delete(self.endpoint)

        with app.app_context():
            count = mongo.db.events.count()
            event = mongo.db.events.find()[0]

        self.assertEqual(count, 1)
        self.assertEqual(event['name'], 'not expired')
