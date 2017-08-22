from django.http.response import Http404, HttpResponseRedirect
from .models import PrivateUrl
from .signals import privateurl_ok, privateurl_fail
from app.views import  current_datetime

dict_private_urls_view = {
    'manage_credit_score':current_datetime}

def privateurl_view(request, action, token):
    obj = PrivateUrl.objects.get_or_none(action, token)
    ok = False
    if not obj or not obj.is_available():
        # fail or expired
        raise Http404
    elif dict_private_urls_view(action):
        return current_datetime(request,token)
        # sucess case
    if not ok:
        raise Http404
    return HttpResponseRedirect('/')


