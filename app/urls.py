from django.conf.urls import url
from app.views.healthcheck import healthcheck
from app.views.home import home
from app.views.index import index
from app.views.api.papers import api_papers


urlpatterns = [
    url(r'^healthcheck$', healthcheck, name='healthcheck'),
    url(r'^$', home, name='home'),
    url(r'^index$', index, name='index'),
    url(r'^api/papers$', api_papers, name='api_papers'),
]
