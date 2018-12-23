from django.urls import path

from app.views.api.paper import api_paper
from app.views.api.papers import api_papers
from app.views.healthcheck import healthcheck
from app.views.home import home
from app.views.index import index

urlpatterns = [
    path('healthcheck', healthcheck, name='healthcheck'),
    path('', home, name='home'),
    path('index',  index, name='index'),
    path('api/papers', api_papers, name='api_papers'),
    path('api/paper/<int:paper_id>', api_paper, name='api_paper'),
]
