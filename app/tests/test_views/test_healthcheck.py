from app.tests.base_testcase import BaseTestCase


class HealthCheckTestCase(BaseTestCase):

    def test_get(self):
        response = self.client.get('/healthcheck')

        self.assertEqual(response.status_code, 200)
