from django.conf.urls import url

from . import views

app_name = 'index'
urlpatterns = [
    url(r'^$', views.index_viewer, name='viewer'),
    url(r'^poster_only/$', views.index_posteronly, name='posteronly'),
    url(r'^load_posters/(?P<res>[0-9]+)/$', views.load_posters, name='load_posters'),
    url(r'^load_posters/$', views.load_posters, name='load_posters'),
    url(r'^load_thumbs/$', views.load_thumbs, name='load_thumbs'),
    url(r'^load_activities/$', views.load_activities, name='load_activities'),
]