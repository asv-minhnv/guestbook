from cPickle import load
import urllib
from django.http import request

from django.http.response import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from google.appengine.api import users

import logging

from guestbook.models import Greeting, guestbook_key, DEFAULT_GUESTBOOK_NAME
class IndexViev(ListView):
    guestbook_name = DEFAULT_GUESTBOOK_NAME
  #   model = Greeting
  # greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)

    greetings_query = Greeting.query(ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
    greetings = greetings_query.fetch(10)

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
    queryset= template_values
    context_object_name= "greetings"
    template_name= "guestbook/main_page.html"

class SignViev(TemplateView):
    def post(self,request):
       # logging.info(request.POST['content'])
       # return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': DEFAULT_GUESTBOOK_NAME}))
        guestbook_name = request.POST.get('guestbook_name')
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = users.get_current_user()

        greeting.content = request.POST.get('content')
        greeting.put()
        return HttpResponseRedirect('/?' + urllib.urlencode({'guestbook_name': guestbook_name}))
