from app.tests.creations.base import CreationBase
from app.models import RssFetchSubject


class CreationRssFetchSubject(CreationBase):

    def create(self, name=None, url=None):
        return RssFetchSubject.objects.create(
            name=name or 'RSS_FETCH_SUBJECT_NAME',
            url=url or 'http://example.com/',
        )
