from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^', include('prismic_app.urls', namespace='prismic'))
)