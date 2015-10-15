from django.conf.urls import patterns,url
from guestbook.views import IndexView, GuestbookView

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view()),
    url(r'^guestbook/$', GuestbookView.as_view()),
)