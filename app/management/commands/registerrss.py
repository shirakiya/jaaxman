from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import RssFetchSubject

RSS_LIST = (
    {
        'name': 'stat.ML',
        'url': 'http://export.arxiv.org/rss/stat.ML',
    },
    {
        'name': 'cs.AI',
        'url': 'http://export.arxiv.org/rss/cs.AI',
    },
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        subjects = {s.name: s for s in RssFetchSubject.objects.all()}

        with transaction.atomic():
            for rss in RSS_LIST:
                if rss['name'] in subjects:
                    continue
                RssFetchSubject.objects.create(**rss)

        self.stdout.write(self.style.SUCCESS('Successfully register RSS.'))
