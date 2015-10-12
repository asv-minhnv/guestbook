from django.conf.urls import patterns, include, url
from guestbook.views import MainView, SignView

urlpatterns = patterns('',
                       (r'^sign/$', SignView.as_view()),
                       (r'^$', MainView.as_view()),
                       )