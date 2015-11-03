from django.conf.urls import patterns,url
# from api.views import IndexView
from django.views.generic import TemplateView

urlpatterns = patterns('',
	url(r'^$', TemplateView.as_view(template_name='guestbook/dojo.html')),


)