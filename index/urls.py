from django.conf.urls import url

from . import views

app_name = 'index'
urlpatterns = [
    url(r'^$', views.index_viewer, name='viewer'),
    url(r'^poster_only/$', views.index_posteronly, name='posteronly'),
]