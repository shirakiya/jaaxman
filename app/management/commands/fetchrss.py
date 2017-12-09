from logging import getLogger
import os
from django.core.management.base import BaseCommand
from django.db import transaction
from jaaxman.exceptions import EnvironmentVariableNotDefineError
from app.lib.rss.arxiv import ArxivRss
from app.lib.slack import Slack
from app.models import RssFetchSubject

logger = getLogger(__name__)


class Command(BaseCommand):

    def _slack(self):
        incoming_webhook_url = os.getenv('SLACK_URL')
        if not incoming_webhook_url:
            raise EnvironmentVariableNotDefineError('SLACK_URL is not defined.')

        return Slack(incoming_webhook_url)

    @transaction.atomic
    def handle(self, *args, **options):
        paper_count = 0
        for subject in RssFetchSubject.objects.all():
            arxiv_rss = ArxivRss(subject)
            papers = arxiv_rss.fetch_and_save()
            paper_count += len(papers)

        message = f'Successfully fetch and save {paper_count} papers from RSS.'
        logger.info(self.style.SUCCESS(message))

        slack = self._slack()
        slack.notify_fetchrss(message)
