import slackweb


class Slack(object):

    def __init__(self, incoming_webhook_url):
        self.slackweb = slackweb.Slack(url=incoming_webhook_url)

    def notify(self, payload):
        self.slackweb.notify(**payload)
