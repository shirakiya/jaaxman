from django.conf.urls import url
from app.views.home import home
from app.views.index import index


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^index$', index, name='index'),
]
