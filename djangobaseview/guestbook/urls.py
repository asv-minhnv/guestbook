from django.conf.urls import patterns,url
from guestbook.views import IndexView, SignView


urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^sign/$', SignView.as_view()),
)