from django.conf.urls import patterns, url
from templateresponsemixin.views import IndexView, SignView

urlpatterns = patterns('',
    url(r'^sign/$', SignView.as_view()),
    url(r'^$', IndexView.as_view()),
)
