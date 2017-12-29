import datetime
import pytz
from unittest.mock import patch, ANY
from parameterized import parameterized
from app.tests.base_testcase import BaseTestCase
from app.models import Paper


class PaperTestCase(BaseTestCase):

    def setUp(self):
        self.rss_fetch_subject = self.creation.rss_fetch_subject()
        self.rss_fetch_history = self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject.id,
        )

    @patch('app.models.paper.Paper._set_translation')
    def test_from_xml(self, _):
        arxiv_paper_item = {
            'title': 'Some title.(arXiv:1611.07078v2 [cs.AI] UPDATED)',
            'abstract': 'ABSTRACT',
            'link': 'LINK',
        }
        result = Paper.from_xml(arxiv_paper_item)

        self.assertIsInstance(result, Paper)
        self.assertEqual(result.title, 'Some title.(arXiv:1611.07078v2 [cs.AI] UPDATED)')
        self.assertEqual(result.abstract, 'ABSTRACT')
        self.assertEqual(result.link, 'LINK')
        self.assertEqual(result.subject, 'cs.AI')
        self.assertEqual(result.submit_type, Paper.SUBMIT_TYPE_UPDATED)

    def test_set_subject(self):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='Paper title. (arXiv:1708.00000 [cs.AI])',
        )
        paper._set_subject()

        self.assertEqual(paper.subject, 'cs.AI')

    def test_set_subject_updated(self):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='Paper title. (arXiv:1708.00000 [cs.AI] UPDATED)',
        )
        paper._set_subject()

        self.assertEqual(paper.subject, 'cs.AI')

    @parameterized.expand([
        ('TITLE([])', Paper.SUBMIT_TYPE_NEW),
        ('TITLE([] UPDATED)', Paper.SUBMIT_TYPE_UPDATED),
        ('TITLE([] CROSS LISTED)', Paper.SUBMIT_TYPE_NEW),
    ])
    def test_set_submit_type_for_new(self, title, expected):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title=title,
        )
        paper.set_submit_type()

        self.assertEqual(paper.submit_type, expected)

    @parameterized.expand([
        ('TITLE([])', False),
        ('TITLE([] UPDATED)', False),
        ('TITLE([] CROSS LISTED)', True),
    ])
    def test_is_cross_listed(self, title, expected):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title=title,
        )
        paper.set_is_cross_listed()

        self.assertEqual(paper.is_cross_listed, expected)

    @patch('app.lib.google_translator.GoogleTranslator.translate')
    def test_set_translation(self, m_translate):
        m_translate.return_value = ['タイトル', '要約']

        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='TITLE',
            abstract='ABSTRACT',
        )
        paper._set_translation()

        m_translate.assert_called_with(['TITLE', 'ABSTRACT'])
        self.assertEqual(paper.title_ja, 'タイトル')
        self.assertEqual(paper.abstract_ja, '要約')

    def test_add_authors_when_given_empty_list(self):
        authors_from_xml = []
        paper = self.creation.paper(rss_fetch_history_id=self.rss_fetch_history.id)
        result = paper.add_authors(authors_from_xml)

        self.assertFalse(result)

    def test_add_authors(self):
        authors_from_xml = [
            {
                'name': 'AUTHOR_NAME_0',
                'link': 'AUTHOR_LINK_0',
            },
            {
                'name': 'AUTHOR_NAME_1',
                'link': 'AUTHOR_LINK_1',
            },
        ]
        paper = self.creation.paper(rss_fetch_history_id=self.rss_fetch_history.id)
        result = paper.add_authors(authors_from_xml)
        authors = paper.authors.all()

        self.assertTrue(result)
        self.assertEqual(len(authors), 2)
        self.assertEqual(authors[0].name, 'AUTHOR_NAME_0')
        self.assertEqual(authors[0].link, 'AUTHOR_LINK_0')
        self.assertEqual(authors[1].name, 'AUTHOR_NAME_1')
        self.assertEqual(authors[1].link, 'AUTHOR_LINK_1')

    def test_dumps(self):
        paper = self.creation.paper(rss_fetch_history_id=self.rss_fetch_history.id)
        author = self.creation.author()
        paper.authors.add(author)
        result = paper.dumps()

        self.assertIsInstance(result['id'], int)
        self.assertIsInstance(result['created_at'], datetime.datetime)
        self.assertIsInstance(result['updated_at'], datetime.datetime)
        self.assertIsInstance(result['authors'][0], dict)
        self.assertEqual(result, {
            'id': ANY,
            'title': 'PAPER_TITLE',
            'title_ja': 'タイトル',
            'abstract': 'ABSTRACT',
            'abstract_ja': '要約',
            'link': 'http://arxiv.org/abs/1708.00000',
            'subject': 'SUBJECT',
            'submit_type': 'new',
            'is_cross_listed': False,
            'created_at': ANY,
            'updated_at': ANY,
            'authors': ANY,
        })

    @parameterized.expand([
        (pytz.timezone('Asia/Tokyo'), '2017-12-24'),
        (pytz.utc, '2017-12-23'),
    ])
    def test_get_fetch_date(self, timezone, expected):
        paper = self.creation.paper(rss_fetch_history_id=self.rss_fetch_history.id)
        paper.created_at = datetime.datetime(2017, 12, 23, 21, 0, 0)
        result = paper.get_fetch_date(timezone)

        self.assertEqual(result, expected)
