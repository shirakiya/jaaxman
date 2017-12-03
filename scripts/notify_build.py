"""Buildしたtarballのファイル名をSlackに通知する"""
import argparse
import os
import slackweb


class Slack(object):

    def __init__(self, incoming_webhook_url):
        self.slackweb = slackweb.Slack(url=incoming_webhook_url)

    def notify(self, payload):
        self.slackweb.notify(**payload)


def build_payload(filename):
    return {
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


def notify_build(filename):
    incoming_webhook_url = os.getenv('SLACK_URL')
    if not incoming_webhook_url:
        raise Exception('"SLACK_URL" must be defined as environment variables.')

    slack = Slack(incoming_webhook_url)
    payload = build_payload(filename)
    slack.notify(payload)

    print('Success to send notification.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('filename', type=str, help='tarball filename')
    args = parser.parse_args()

    notify_build(args.filename)
