from tests.testcases import AppTestCase
from datahub.main import redis


class ApiListTestCase(AppTestCase):

    def test_get_invalid_key(self):
        response = self.app.get('/invalid')

        self.assertEqual(response.status_code, 400)

    def test_get_detail(self):
        redis.set('test', 2)

        response = self.app.get('/test')

        self.assertEqual(response.status_code, 200)
        self.assertEqual({
            'value': 2
        }, response.json)
