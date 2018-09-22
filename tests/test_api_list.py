import json
from tests.testcases import AppTestCase


class ApiListTestCase(AppTestCase):

    def add_data(self, data):
        self.app.post(
            self.endpoint,
            data=json.dumps(data),
            content_type='application/json'
        )

    def test_get_empty_list(self):
        response = self.app.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_list(self):
        for i in range(1, 4):
            self.add_data({
                'name': 'Name %s' % i,
                'value': i
            })

        response = self.app.get(self.endpoint)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 3)
        self.assertIn('Name 1', response.json)
        self.assertIn('Name 2', response.json)
        self.assertIn('Name 3', response.json)

    def test_filter_by_pattern(self):
        self.add_data({
            'name': 'sensor:temperature',
            'value': 64
        })
        self.add_data({
            'name': 'event:face_recognized',
            'value': 64
        })

        response = self.app.get(self.endpoint + '?filter=sensor:*')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertIn('sensor:temperature', response.json)
