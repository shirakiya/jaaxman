from django.conf import settings
import twitter
from jaaxman.exceptions import EnvironmentVariableNotDefineError


class Twitter(object):

    def __init__(self):
        consumer_key = settings.TWITTER_CONSUMER_KEY
        consumer_secret = settings.TWITTER_CONSUMER_SECRET
        access_token_key = settings.TWITTER_ACCESS_TOKEN_KEY
        access_token_secret = settings.TWITTER_ACCESS_TOKEN_SECRET

        self._validate_credentials(
            consumer_key,
            consumer_secret,
            access_token_key,
            access_token_secret,
        )

        self._api = twitter.Api(consumer_key=consumer_key,
                                consumer_secret=consumer_secret,
                                access_token_key=access_token_key,
                                access_token_secret=access_token_secret)

    def _validate_credentials(self, consumer_key, consumer_secret, access_token_key, access_token_secret):
        not_defined_credentials = {
            'TWITTER_CONSUMER_KEY': False,
            'TWITTER_CONSUMER_SECRET': False,
            'TWITTER_ACCESS_TOKEN_KEY': False,
            'TWITTER_ACCESS_TOKEN_SECRET': False,
        }

        if not consumer_key:
            not_defined_credentials['TWITTER_CONSUMER_KEY'] = True
        if not consumer_secret:
            not_defined_credentials['TWITTER_CONSUMER_SECRET'] = True
        if not access_token_key:
            not_defined_credentials['TWITTER_ACCESS_TOKEN_KEY'] = True
        if not access_token_secret:
            not_defined_credentials['TWITTER_ACCESS_TOKEN_SECRET'] = True

        if any(is_not_defined for is_not_defined in not_defined_credentials.values()):
            not_defined_keys = ','.join([k for k, v in not_defined_credentials.items() if v])
            raise EnvironmentVariableNotDefineError(f'Not defined {not_defined_keys}.')

    def post_tweet(self, text):
        self._api.PostUpdate(text)
