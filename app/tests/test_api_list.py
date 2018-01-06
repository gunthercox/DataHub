import json
from tests.testcases import AppTestCase


class ApiListTestCase(AppTestCase):

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
