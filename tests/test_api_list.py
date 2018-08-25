import json
from tests.testcases import AppTestCase


class ApiListTestCase(AppTestCase):

    def test_get_empty_list(self):
        response = self.app.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

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

        self.assertEqual(len(response.json), 3)
        self.assertIn('Name 1', response.json)
        self.assertIn('Name 2', response.json)
        self.assertIn('Name 3', response.json)
