from django.conf.urls import patterns,url
from guestbook.views import IndexView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view()),
)