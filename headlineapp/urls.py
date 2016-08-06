from django.conf.urls import patterns, url
from headlineapp import views

urlpatterns = patterns('',
    url(r'^$', views.base, name='base'),
    url(r'^(?P<headline_id>\d+)/$', views.item, name='item'),
    url(r'^(?P<headline_id>\d+)$', views.item_redirect, name='item_redirect'),
)
