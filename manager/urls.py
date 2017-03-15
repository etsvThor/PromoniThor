from django.conf.urls import url

from . import views

app_name = 'manager'
urlpatterns = [
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^about/$', views.about, name='about'),
    url(r'^clearcache/$', views.clear_cache, name='clearcache'),
    url(r'^upload/(?P<ty>[a-z]{1})/$', views.upload, name='upload'),
    url(r'^list/$', views.list, name='list'),
    url(r'^edit/(?P<poster>[0-9]+)/$', views.edit, name='edit'),
    url(r'^delete/(?P<poster>[0-9]+)/$', views.delete, name='delete'),
    url(r'^$', views.index, name='index')
]