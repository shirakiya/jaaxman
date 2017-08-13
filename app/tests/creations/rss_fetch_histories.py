from app.tests.creations.base import CreationBase
from app.models import RssFetchHistory


class CreationRssFetchHistory(CreationBase):

    def create(self, rss_fetch_subject_id=1, date=None):
        return RssFetchHistory.objects.create(
            rss_fetch_subject_id=rss_fetch_subject_id,
            date=date or '2017-08-01T20:30:00-05:00',
        )
