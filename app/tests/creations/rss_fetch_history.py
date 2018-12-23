from app.models import RssFetchHistory
from app.tests.creations.base import CreationBase


class CreationRssFetchHistory(CreationBase):

    def create(self, rss_fetch_subject_id=1, date=None, is_duplicated=False):
        return RssFetchHistory.objects.create(
            rss_fetch_subject_id=rss_fetch_subject_id,
            date=date or '2017-08-01T20:30:00-05:00',
            is_duplicated=is_duplicated,
        )
