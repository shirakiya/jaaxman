from django.conf import settings
from django.http import HttpResponse

from jaaxman.exceptions import EnvironmentVariableNotDefineError


class HttpResponseBadRequest(HttpResponse):
    status_code = 400


class HttpResponseUnauthorized(HttpResponse):
    status_code = 401


class AuthorizationMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

        self.token = settings.API_TOKEN
        if not self.token and self.enabled:
            raise EnvironmentVariableNotDefineError(
                'Environment variable "API_TOKEN" is not defined.')

    def __call__(self, request):

        response = self.get_response(request)

        return response

    @property
    def enabled(self):
        return settings.RUN_MODE == settings.RUN_MODE_PRODUCTION

    def _response_400(self, realm='invalid_request'):
        response = HttpResponseBadRequest()

        response['WWW-Authenticate'] = f'Bearer realm="{realm}"'

        return response

    def _response_401(self, realm):
        response = HttpResponseUnauthorized()

        response['WWW-Authenticate'] = f'Bearer realm="{realm}"'

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if not self.enabled or not view_func.__name__.startswith('api_jobs'):
            return None

        authorization = request.META.get('HTTP_AUTHORIZATION', '')
        splited = authorization.split(' ', 1)

        if len(splited) != 2 or not splited[1]:
            return self._response_401('production')

        schema, user_token = splited

        if schema != 'Bearer':
            return self._response_400()
        if self.token != user_token:
            return self._response_401('invalid_token')

        return None
