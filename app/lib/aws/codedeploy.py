from .base import Aws
from jaaxman.exceptions import InvalidDeploymentRoleError


class CodeDeploy(object):

    AVAILABLE_ROLES = (
        'app',
        'job',
    )
    APPLICATION_NAME = 'jaaxman'

    def __init__(self, role):
        self.role = self._validate_role(role)
        self.client = Aws.get_codedeploy_client()

    def _validate_role(self, role):
        if role not in self.AVAILABLE_ROLES:
            raise InvalidDeploymentRoleError('"role" must be "app" or "job".')
        return role

    def _get_deployment_group_name(self):
        return f'{self.APPLICATION_NAME}-{self.role}'

    def _get_revision_key(self, revision):
        return f'app/{revision}'

    def deploy(self, revision):
        return self.client.create_deployment(
            applicationName=self.APPLICATION_NAME,
            deploymentGroupName=self._get_deployment_group_name(),
            revision={
                'revisionType': 'S3',
                's3Location': {
                    'bucket': 'jaaxman-production-infla',
                    'key': self._get_revision_key(revision),
                    'bundleType': 'tgz',
                },
            }
        )
