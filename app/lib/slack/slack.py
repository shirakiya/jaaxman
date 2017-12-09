import slackweb


class Slack(object):

    def __init__(self, incoming_webhook_url):
        self.slackweb = slackweb.Slack(url=incoming_webhook_url)

    def notify(self, payload):
        self.slackweb.notify(**payload)

    def notify_fetchrss(self, message):
        payload = {
            'username': 'Jaaxman',
            'channel': '#dev_notifications',
            'attachments': [{
                'title': 'job (fetchrss)',
                'text': message,
                'color': 'good',
                'mrkdwn_in': ['text', 'pretext'],
            }],
        }
        return self.notify(payload)
