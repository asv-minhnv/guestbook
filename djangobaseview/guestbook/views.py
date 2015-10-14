import urllib
from google.appengine.api import users
from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME

class IndexView(TemplateView):

    template_name = "guestbook/main_page.html"
    def post(self, request, *args, **kwargs):
        guestbook_name = request.POST.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = users.get_current_user()
        greeting.content = request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        guestbook_name = DEFAULT_GUESTBOOK_NAME
        greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings=greetings_query.fetch(10)
        if users.get_current_user():
            url = users.create_logout_url('/')
            url_linktext = 'Logout'
        else:
            url = users.create_login_url('/')
            url_linktext = 'Login'

        template_values = {
            'greetings': greetings,
            'guestbook_name': guestbook_name,
            'url': url,
            'url_linktext': url_linktext,
        }
        context['greetings'] = template_values
        return context

class SignView(TemplateView):
    def post(self, request):
        guestbook_name = request.POST.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = users.get_current_user()
        greeting.content = request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
