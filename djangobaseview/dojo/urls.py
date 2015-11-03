from django.conf.urls import patterns,url
# from api.views import IndexView
from api.restful import GetListView,ResourceSinge

urlpatterns = patterns('',
	url(r'^guestbook/(?P<guestbook_name>.+)/greeting/(?P<id>\d+)$', ResourceSinge.as_view()),
	url(r'^guestbook/(?P<guestbook_name>).+/greeting/$', GetListView.as_view()),

)