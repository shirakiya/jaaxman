#!/usr/bin/env python
import argparse
import hashlib
import json
from copy import deepcopy

import boto3
from loguru import logger

reuse_settings_keys = (
    'cpu',
    'executionRoleArn',
    'family',
    'memory',
    'networkMode',
    'placementConstraints',
    'requiresCompatibilities',
    'taskRoleArn',
    'volumes',
)


def update_app_task_definition(ecs_client, backend_image: str, nginx_image: str) -> dict:
    response = ecs_client.describe_task_definition(taskDefinition='jaaxman-app')
    logger.debug(response)

    task_definition = response['taskDefinition']

    app_task_definition = {
        'containerDefinitions': [],
    }  # type: dict
    for reuse_settings_key in reuse_settings_keys:
        app_task_definition[reuse_settings_key] = task_definition[reuse_settings_key]

    for container_definition in task_definition['containerDefinitions']:
        if container_definition['name'] == 'app':
            container_definition['image'] = backend_image
        elif container_definition['name'] == 'nginx':
            container_definition['image'] = nginx_image

        app_task_definition['containerDefinitions'].append(container_definition)

    logger.info(app_task_definition)

    response = ecs_client.register_task_definition(**app_task_definition)
    logger.debug(response)

    return response['taskDefinition']


def update_job_task_definition(ecs_client, backend_image: str) -> dict:
    response = ecs_client.describe_task_definition(taskDefinition='jaaxman-job')
    logger.debug(response)

    task_definition = response['taskDefinition']
    job_task_definition = {
        'containerDefinitions': [],
    }  # type: dict
    for reuse_settings_key in reuse_settings_keys:
        job_task_definition[reuse_settings_key] = task_definition[reuse_settings_key]

    for container_definition in task_definition['containerDefinitions']:
        if container_definition['name'] == 'app':
            container_definition['image'] = backend_image

        job_task_definition['containerDefinitions'].append(container_definition)

    logger.info(job_task_definition)

    response = ecs_client.register_task_definition(**job_task_definition)
    logger.debug(response)

    return response['taskDefinition']


def update_task_definition(ecs_client, backend_image: str, nginx_image: str) -> dict:
    app_task_definition = update_app_task_definition(ecs_client, backend_image, nginx_image)
    job_task_definition = update_job_task_definition(ecs_client, backend_image)

    return {
        'app': app_task_definition,
        'job': job_task_definition,
    }


def create_migration_task(ecs_client, task_definition: dict) -> None:
    # TODO: hard coding, too disgraceful...
    logger.debug(task_definition)
    response = ecs_client.run_task(
        cluster='jaaxman',
        taskDefinition=task_definition['taskDefinitionArn'],
        overrides={
            'containerOverrides': [{
                'name': 'app',
                'command': ['python', 'manage.py', 'migrate'],
            }],
        },
        count=1,
        launchType='FARGATE',
        platformVersion='LATEST',
        networkConfiguration={
            'awsvpcConfiguration': {
                'subnets': [
                    'subnet-6a5bfa23',
                    'subnet-739d852b',
                ],
                'securityGroups': [
                    'sg-7031c709',
                ],
                'assignPublicIp': 'ENABLED',
            },
        },
    )
    logger.debug(response)


def _sha256(value):
    return hashlib.sha256(value.encode()).hexdigest()


def deploy_app_service(cd_client, task_definition: dict) -> None:
    task_definition_arn = task_definition['taskDefinitionArn']

    app_spec_content = {
      'version': 1,
      'Resources': [
        {
          'TargetService': {
            'Type': 'AWS::ECS::Service',
            'Properties': {
              'TaskDefinition': task_definition_arn,
              'LoadBalancerInfo': {
                'ContainerName': 'nginx',
                'ContainerPort': 80,
              }
            }
          }
        }
      ]
    }  # type: dict
    app_spec_content_json = json.dumps(app_spec_content)

    response = cd_client.create_deployment(
        applicationName='AppECS-jaaxman-jaaxman-app',
        deploymentGroupName='DgpECS-jaaxman-jaaxman-app',
        description=f'Deploy using TaskDefinition={task_definition_arn}',
        revision={
            'revisionType': 'AppSpecContent',
            'appSpecContent': {
                'content': app_spec_content_json,
                'sha256': _sha256(app_spec_content_json),
            },
        },
        deploymentConfigName='CodeDeployDefault.ECSAllAtOnce',
    )

    deployment_id = response['deploymentId']
    logger.info(f'deploymentId: {deployment_id}')


def update_job_scheduled_task(events_client, task_definition: dict) -> None:
    rule_name = 'jaaxman-fetchrss'

    response = events_client.list_targets_by_rule(Rule=rule_name)
    logger.debug(response)

    target = response['Targets'][0]
    new_ecs_parameters = deepcopy(target['EcsParameters'])
    new_ecs_parameters['TaskDefinitionArn'] = task_definition['taskDefinitionArn']

    response = events_client.put_targets(
        Rule='jaaxman-fetchrss',
        Targets=[{
            'Id': target['Id'],
            'Arn': target['Arn'],
            'RoleArn': target['RoleArn'],
            'EcsParameters': new_ecs_parameters
        }]
    )


def deploy(backend_image: str, nginx_image: str) -> None:
    sess = boto3.session.Session()
    ecs_client = sess.client('ecs')
    cd_client = sess.client('codedeploy')
    events_client = sess.client('events')

    task_definitions = update_task_definition(ecs_client, backend_image, nginx_image)

    create_migration_task(ecs_client, task_definitions['job'])
    update_job_scheduled_task(events_client, task_definitions['job'])
    deploy_app_service(cd_client, task_definitions['app'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('backend_image', type=str)
    parser.add_argument('nginx_image', type=str)
    args = parser.parse_args()

    deploy(args.backend_image, args.nginx_image)
