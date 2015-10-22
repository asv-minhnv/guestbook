from django.conf.urls import patterns,url
from guestbook.views import IndexView, SignView, DeleteView, SendmailView, EditView

urlpatterns = patterns('',
	url(r'^guestbook/?P<guestbook_name>/greeting$', IndexView.as_view()),
)