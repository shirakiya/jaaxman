from logging import getLogger

from django.core.management.base import BaseCommand

from app.lib.aws import CodeDeploy

logger = getLogger(__name__)


class Command(BaseCommand):

    help = 'Execute deployment via CodeDeploy'

    def add_arguments(self, parser):
        parser.add_argument('role', type=str, choices=CodeDeploy.AVAILABLE_ROLES,
                            help='deployment role.')
        parser.add_argument('revision', type=str,
                            help='revision file name stored in S3. e.g. "jaaxman-20171123135308.tar.gz"')

    def handle(self, *args, **options):
        role = options['role']
        revision = options['revision']

        try:
            codedeploy = CodeDeploy(role)
            response = codedeploy.deploy(revision)
        except Exception as e:
            logger.critical(self.style.ERROR('Failed to start deployment.'))
            raise e

        message_1 = 'Success to start deployment via CodeDeploy.'
        message_2 = f'deploymentId: {response["deploymentId"]}'
        logger.info(self.style.SUCCESS(message_1))
        logger.info(self.style.SUCCESS(message_2))
