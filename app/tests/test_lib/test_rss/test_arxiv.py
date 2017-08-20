from unittest.mock import Mock, patch
import requests
from app.tests.base_testcase import BaseTestCase
from app.exceptions import RssFetchError, RssParseError
from app.models import RssFetchHistory
from app.lib.rss.arxiv import ArxivRss


class ArxivRssTestCase(BaseTestCase):

    def setUp(self):
        self.rss_fetch_subject = self.creation.rss_fetch_subject()

    @patch('requests.get')
    def test_request(self, m):
        m.return_value = requests.Response()
        arxiv_rss = ArxivRss(self.rss_fetch_subject)
        result = arxiv_rss._request()

        self.assertIsInstance(result, requests.Response)

    @patch('requests.get')
    def test_request_with_timeout(self, m):
        m.side_effect = requests.Timeout
        arxiv_rss = ArxivRss(self.rss_fetch_subject)

        with self.assertRaises(RssFetchError):
            arxiv_rss._request()

        self.assertEqual(arxiv_rss.request_count, arxiv_rss.RETRY_COUNT)

    @patch('requests.get')
    def test_request_with_unexpected_error(self, m):
        m.side_effect = requests.HTTPError
        arxiv_rss = ArxivRss(self.rss_fetch_subject)

        with self.assertRaises(RssFetchError):
            arxiv_rss._request()

    @patch('requests.get')
    def test_fetch(self, m):
        m.return_value = Mock(text='RESPONSE_TEXT')
        arxiv_rss = ArxivRss(self.rss_fetch_subject)
        result = arxiv_rss.fetch()

        self.assertEqual(result, 'RESPONSE_TEXT')

    @patch('app.lib.xml.arxiv.ArxivXml.get_date')
    def test_fetch_and_save_with_g(self, m):
        m.return_value = None
        arxiv_rss = ArxivRss(self.rss_fetch_subject)
        arxiv_rss.fetch = Mock(return_value='<rdf:RDF></rdf:RDF>')

        with self.assertRaises(RssParseError):
            arxiv_rss.fetch_and_save()

    @patch('app.lib.xml.arxiv.ArxivXml.get_date')
    def test_fetch_and_save_when_already_saved_same_date_rss_fetch_history(self, m):
        m.return_value = '2017-08-01T20:30:00-05:00'
        self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject.id,
            date='2017-08-01T20:30:00-05:00',
        )
        arxiv_rss = ArxivRss(self.rss_fetch_subject)
        arxiv_rss.fetch = Mock(return_value='<rdf:RDF></rdf:RDF>')
        result = arxiv_rss.fetch_and_save()
        rss_fetch_histories = RssFetchHistory.objects.all()

        self.assertEqual(len(rss_fetch_histories), 2)
        self.assertTrue(rss_fetch_histories[1].is_duplicated)
        self.assertEqual(result, [])

    @patch('app.lib.xml.arxiv.ArxivXml.get_date')
    def test_fetch_and_save_with_saving_rss_fetch_history(self, m):
        m.return_value = '2017-08-01T20:30:00-05:00'
        arxiv_rss = ArxivRss(self.rss_fetch_subject)
        arxiv_rss.fetch = Mock(return_value='<rdf:RDF></rdf:RDF>')
        result = arxiv_rss.fetch_and_save()
        rss_fetch_histories = RssFetchHistory.objects.all()

        self.assertEqual(len(rss_fetch_histories), 1)
        self.assertEqual(rss_fetch_histories[0].date, '2017-08-01T20:30:00-05:00')
        self.assertEqual(result, [])

    @patch('app.lib.xml.arxiv.ArxivXml.get_date')
    @patch('app.lib.xml.arxiv.ArxivXml.get_paper_items')
    @patch('app.lib.google_translator.GoogleTranslator.translate')
    def test_fetch_and_save_papers(self, m_translate, m_get_paper_items, m_get_date):
        m_get_date.return_value = '2017-08-01T20:30:00-05:00'
        m_get_paper_items.return_value = [
            {
                'title': 'TITLE_0([cs.AI])',
                'abstract': 'ABSTRACT_0',
                'link': 'LINK_0',
                'authors': [],
            },
            {
                'title': 'TITLE_1([stat.ML])',
                'abstract': 'ABSTRACT_1',
                'link': 'LINK_1',
                'authors': [],
            },
        ]
        m_translate.return_value = ['タイトル', '要約']

        arxiv_rss = ArxivRss(self.rss_fetch_subject)
        arxiv_rss.fetch = Mock(return_value='<rdf:RDF></rdf:RDF>')
        result = arxiv_rss.fetch_and_save()
        rss_fetch_histories = RssFetchHistory.objects.first()
        papers = rss_fetch_histories.papers.all()

        self.assertEqual(len(result), 2)
        self.assertEqual(len(papers), 2)
        self.assertEqual(result, list(papers))

        self.assertEqual(result[0].title, 'TITLE_0([cs.AI])')
        self.assertEqual(result[0].title_ja, 'タイトル')
        self.assertEqual(result[0].abstract, 'ABSTRACT_0')
        self.assertEqual(result[0].abstract_ja, '要約')
        self.assertEqual(result[0].link, 'LINK_0')
        self.assertEqual(result[0].subject, 'cs.AI')

        self.assertEqual(result[1].title, 'TITLE_1([stat.ML])')
        self.assertEqual(result[1].title_ja, 'タイトル')
        self.assertEqual(result[1].abstract, 'ABSTRACT_1')
        self.assertEqual(result[1].abstract_ja, '要約')
        self.assertEqual(result[1].link, 'LINK_1')
        self.assertEqual(result[1].subject, 'stat.ML')
