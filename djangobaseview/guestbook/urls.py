from django.conf.urls import patterns,url
from guestbook.views import IndexView, DetailView, DeleteView, EditView

urlpatterns = patterns('',
	url(r'^$', IndexView.as_view()),
	url(r'^detail/$', DetailView.as_view()),
	url(r'^delete/$', DeleteView.as_view()),
	url(r'^edit/$', EditView.as_view()),
)