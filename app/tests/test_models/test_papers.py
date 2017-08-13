from app.tests.base_testcase import BaseTestCase


class PaperTestCase(BaseTestCase):

    def setUp(self):
        self.rss_fetch_subject = self.creation.rss_fetch_subject()
        self.rss_fetch_history = self.creation.rss_fetch_history(
            rss_fetch_subject_id=self.rss_fetch_subject.id,
        )

    def test_set_subject(self):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='paper title. (arXiv:1708.00000 [cs.AI])',
        )
        paper.set_subject()

        self.assertEqual(paper.subject, 'cs.AI')

    def test_set_subject_updated(self):
        paper = self.creation.paper(
            rss_fetch_history_id=self.rss_fetch_history.id,
            title='paper title. (arXiv:1708.00000 [cs.AI] UPDATED)',
        )
        paper.set_subject()

        self.assertEqual(paper.subject, 'cs.AI')
