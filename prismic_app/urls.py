from django.conf.urls import patterns, url

from prismic_app import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^document/(?P<id>[-_a-zA-Z0-9]{16})/(?P<slug>.*)', views.detail, name='document'))
