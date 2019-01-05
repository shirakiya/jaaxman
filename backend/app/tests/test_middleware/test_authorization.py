from unittest.mock import Mock, patch

from django.conf import settings
from django.http import HttpRequest
from parameterized import parameterized

from app.middleware.authorization import AuthorizationMiddleware, HttpResponseBadRequest, HttpResponseUnauthorized
from app.tests.base_testcase import BaseTestCase
from jaaxman.exceptions import EnvironmentVariableNotDefineError


class AuthorizationMiddlewareTestCase(BaseTestCase):

    @patch('app.middleware.authorization.settings')
    def test_init_in_development_and_API_TOKEN_defined(self, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = settings.RUN_MODE_DEVELOPMENT
        m_settings.API_TOKEN = 'SOME_API_TOKEN'

        self.assertIsInstance(AuthorizationMiddleware(Mock()), AuthorizationMiddleware)

    @patch('app.middleware.authorization.settings')
    def test_init_in_development_and_API_TOKEN_not_defined(self, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = settings.RUN_MODE_DEVELOPMENT
        m_settings.API_TOKEN = None

        self.assertIsInstance(AuthorizationMiddleware(Mock()), AuthorizationMiddleware)

    @patch('app.middleware.authorization.settings')
    def test_init_in_production_and_API_TOKEN_defined(self, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = settings.RUN_MODE_PRODUCTION
        m_settings.API_TOKEN = 'SOME_API_TOKEN'

        self.assertIsInstance(AuthorizationMiddleware(Mock()), AuthorizationMiddleware)

    @patch('app.middleware.authorization.settings')
    def test_init_in_production_and_API_TOKEN_not_defined(self, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = settings.RUN_MODE_PRODUCTION
        m_settings.API_TOKEN = None

        with self.assertRaises(EnvironmentVariableNotDefineError):
            AuthorizationMiddleware(Mock())

    @parameterized.expand([
        (settings.RUN_MODE_DEVELOPMENT, False),
        (settings.RUN_MODE_PRODUCTION, True),
    ])
    @patch('app.middleware.authorization.settings')
    def test_enabled(self, run_mode, expected, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = run_mode
        m_settings.API_TOKEN = 'SOME_API_TOKEN'

        am = AuthorizationMiddleware(Mock())

        self.assertEqual(am.enabled, expected)

    def test_response_400(self):
        am = AuthorizationMiddleware(Mock())
        result = am._response_400()

        self.assertIsInstance(result, HttpResponseBadRequest)
        self.assertEqual(result._headers['www-authenticate'],
                         ('WWW-Authenticate', 'Bearer realm="invalid_request"'))

    def test_response_400_given_realm(self):
        am = AuthorizationMiddleware(Mock())
        result = am._response_400('TEST')

        self.assertIsInstance(result, HttpResponseBadRequest)
        self.assertEqual(result._headers['www-authenticate'],
                         ('WWW-Authenticate', 'Bearer realm="TEST"'))

    def test_response_401(self):
        am = AuthorizationMiddleware(Mock())
        result = am._response_401('TEST')

        self.assertIsInstance(result, HttpResponseUnauthorized)
        self.assertEqual(result._headers['www-authenticate'],
                         ('WWW-Authenticate', 'Bearer realm="TEST"'))

    @patch('app.middleware.authorization.settings')
    def test_process_view_with_valid_authorization(self, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = settings.RUN_MODE_PRODUCTION
        view_func = Mock(__name__='api_jobs_fetchrss')

        request = HttpRequest()
        request.META = {
            'HTTP_AUTHORIZATION': 'Bearer API_TOKEN',
        }

        am = AuthorizationMiddleware(Mock())
        am.token = 'API_TOKEN'

        result = am.process_view(request, view_func, Mock(), Mock())

        self.assertEqual(result, None)

    @patch('app.middleware.authorization.settings')
    def test_process_view_when_not_request_api_jobs(self, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = settings.RUN_MODE_PRODUCTION
        view_func = Mock(__name__='api_papers')

        request = HttpRequest()
        am = AuthorizationMiddleware(Mock())

        result = am.process_view(request, view_func, Mock(), Mock())

        self.assertEqual(result, None)

    @parameterized.expand([
        ('', HttpResponseUnauthorized),
        ('Bearer ', HttpResponseUnauthorized),
        ('API_TOKEN', HttpResponseUnauthorized),
        ('TOKEN API_TOKEN', HttpResponseBadRequest),
        ('Bearer INVALID_API_TOKEN', HttpResponseUnauthorized),
    ])
    @patch('app.middleware.authorization.settings')
    def test_process_view_invalid_authorization(self, authorization, expected_instance, m_settings):
        m_settings.RUN_MODE_PRODUCTION = settings.RUN_MODE_PRODUCTION
        m_settings.RUN_MODE = settings.RUN_MODE_PRODUCTION
        view_func = Mock(__name__='api_jobs_fetchrss')

        request = HttpRequest()
        request.META = {
            'HTTP_AUTHORIZATION': authorization,
        }

        am = AuthorizationMiddleware(Mock())
        am.token = 'API_TOKEN'

        result = am.process_view(request, view_func, Mock(), Mock())

        self.assertIsInstance(result, expected_instance)
