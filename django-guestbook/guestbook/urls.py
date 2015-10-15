from django.conf.urls import patterns, include, url
from guestbook.views import MainView, SignView, send_mail, DeleteView

urlpatterns = patterns('',
    (r'^sign/$', SignView.as_view()),
    (r'^delete/([0-9]{4})/$', DeleteView.as_view()),
    (r'^sendmail/$', send_mail),
    (r'^$', MainView.as_view()),
)