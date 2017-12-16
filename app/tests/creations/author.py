from app.tests.creations.base import CreationBase
from app.models import Author


class CreationAuthor(CreationBase):

    def create(self, name=None, link=None):
        return Author.objects.create(
            name=name or 'AUTHOR_NAME',
            link=link or 'AUTHOR_LINK',
        )
