from django.conf.urls import url

from . import views

app_name = 'changelog'
urlpatterns = [
    url(r'^$', views.list, name='changelog'),
    url(r'^user/(?P<user>[0-9]+)/$', views.list_user, name='user'),
    url(r'^poster/(?P<poster>[0-9]+)/$', views.list_poster, name='poster'),
]