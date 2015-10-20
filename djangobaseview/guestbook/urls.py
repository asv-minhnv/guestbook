from django.conf.urls import patterns,url
from guestbook.views import IndexView, SignView, SendmailView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view()),
	url(r'^sign/$', SignView.as_view()),
	url(r'^sendmail/$', SendmailView.as_view()),
)