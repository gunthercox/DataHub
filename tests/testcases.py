from unittest import TestCase
from datahub.main import app, redis


class AppTestCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.endpoint = '/'

    def tearDown(self):
        redis.flushdb()
