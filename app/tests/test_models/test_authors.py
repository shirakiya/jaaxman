import datetime
from app.tests.base_testcase import BaseTestCase


class AuthorsTestCase(BaseTestCase):

    def setUp(self):
        self.author = self.creation.author()

    def test_dumps(self):
        result = self.author.dumps()

        self.assertIsInstance(result['id'], int)
        self.assertEqual(result['name'], 'AUTHOR_NAME')
        self.assertEqual(result['link'], 'AUTHOR_LINK')
        self.assertIsInstance(result['created_at'], datetime.datetime)
        self.assertIsInstance(result['updated_at'], datetime.datetime)
