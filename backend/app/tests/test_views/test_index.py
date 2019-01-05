from app.tests.base_testcase import BaseTestCase


class ViewIndexTestCase(BaseTestCase):

    def test_get(self):
        response = self.client.get('/index')

        self.assertRedirects(response, '/', status_code=302)
