from logging import getLogger
from django.core.management.base import BaseCommand
from django.db import transaction
from app.lib.rss.arxiv import ArxivRss
from app.models import RssFetchSubject

logger = getLogger(__name__)


class Command(BaseCommand):

    @transaction.atomic
    def handle(self, *args, **options):
        paper_count = 0
        for subject in RssFetchSubject.objects.all():
            arxiv_rss = ArxivRss(subject)
            papers = arxiv_rss.fetch_and_save()
            paper_count += len(papers)

        message = f'Successfully fetch and save {paper_count} papers from RSS.'
        logger.info(self.style.SUCCESS(message))
