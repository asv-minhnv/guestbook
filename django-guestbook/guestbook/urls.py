from django.conf.urls import patterns, include, url
from guestbook.views import MainView, SignView, send_mail

urlpatterns = patterns('',
    (r'^sign/$', SignView.as_view()),
     (r'^sendmail/$', send_mail),
    (r'^$', MainView.as_view()),
)