from app.tests.creations.base import CreationBase
from app.models import Paper


class CreationPaper(CreationBase):

    def create(self, rss_fetch_history_id=1, title=None, title_ja=None,
               abstract=None, abstract_ja=None, link=None, subject=None,
               submit_type=None):
        return Paper.objects.create(
            rss_fetch_history_id=rss_fetch_history_id,
            title=title or 'PAPER_TITLE',
            title_ja=title_ja or 'タイトル',
            abstract=abstract or 'ABSTRACT',
            abstract_ja=abstract_ja or '要約',
            link=link or 'http://arxiv.org/abs/1708.00000',
            subject=subject or 'SUBJECT',
            submit_type=submit_type or 'new',
        )
