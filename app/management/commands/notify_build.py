from logging import getLogger
import os
from django.core.management.base import BaseCommand
from app.lib.slack import Slack

logger = getLogger(__name__)


class Command(BaseCommand):

    help = 'Notify build result'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str, help='tarball filename')

    def handle(self, *args, **options):
        incoming_webhook_url = os.getenv('SLACK_URL')
        if not incoming_webhook_url:
            logger.critical(self.style.ERROR('"SLACK_URL" must be defined as environment variables.'))
            return

        filename = options['filename']
        slack = Slack(incoming_webhook_url)

        payload = {
            'username': 'Build Notification (CircleCI)',
            'channel': '#dev_notifications',
            'icon_emoji': ':circle_ci:',
            'attachments': [{
                'title': 'Build Notification',
                'text': f'Build file: {filename}',
                'color': 'good',
                'mrkdwn_in': ['text', 'pretext'],
            }],
        }
        slack.notify(payload)

        logger.info(self.style.SUCCESS('Success to send notification.'))
