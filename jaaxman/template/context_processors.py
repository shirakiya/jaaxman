from django.conf import settings


def common(request):
    return {
        'RUN_MODE':  settings.RUN_MODE,
        'production': settings.RUN_MODE == settings.RUN_MODE_PRODUCTION,
        'development': settings.RUN_MODE == settings.RUN_MODE_DEVELOPMENT,
        'test': settings.RUN_MODE == settings.RUN_MODE_TEST,
    }
