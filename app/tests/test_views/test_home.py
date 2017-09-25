from app.tests.base_testcase import BaseTestCase


class ViewHomeTestCase(BaseTestCase):

    def test_get(self):
        response = self.client.get('/')

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
