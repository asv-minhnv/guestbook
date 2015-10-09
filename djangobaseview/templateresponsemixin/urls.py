from django.conf.urls import patterns,url
from templateresponsemixin.views import IndexViev, SignViev


urlpatterns = patterns('',
    url(r'^$', IndexViev.as_view()),
    url(r'^sign/$', SignViev.as_view()),
)