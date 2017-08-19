import requests
from app.exceptions import RssFetchError, RssParseError
from app.lib.xml.arxiv import ArxivXml
from app.models import RssFetchSubject, RssFetchHistory, Paper


class ArxivRss(object):

    RETRY_COUNT = 3

    def __init__(self, rss_fetch_subject):
        if not isinstance(rss_fetch_subject, RssFetchSubject):
            raise TypeError('Must be given RssFetchSubject instance.')

        self._subject = rss_fetch_subject
        self.request_count = 0

    def _request(self):
        try:
            return requests.get(self._subject.url, timeout=10)
        except requests.Timeout:
            self.request_count += 1
            if self.request_count >= self.RETRY_COUNT:
                raise RssFetchError(f'Request timeout and retry over {self.RETRY_COUNT} times.')
            else:
                return self._request()
        except requests.RequestException as e:
            raise RssFetchError(str(e))

    def fetch(self):
        res = self._request()
        return res.text

    def fetch_and_save(self):
        rss_text = self.fetch()
        arxiv_xml = ArxivXml(rss_text)
        date = arxiv_xml.get_date()
        if not date:
            raise RssParseError('Could not parse dc:date.')
        if RssFetchHistory.exists(self._subject.id, date):
            return []

        rss_fetch_history = self._subject.rss_fetch_histories.create(date=date)

        papers = []
        for paper_item in arxiv_xml.get_paper_items():
            paper = Paper.from_xml(paper_item)
            rss_fetch_history.papers.add(paper, bulk=False)
            # paper.add_authors(paper_item['authors'])
            papers.append(paper)

        return papers
