from django.conf.urls import url
from . import api


urlpatterns = [
    url(r'^(?i)api/groups/CreditGroupCreateApi/', api.CreditGroupCreateApi.as_view()),
    url(r'^(?i)api/groups/CreditGroupRetrieveUpdateAPI/(?P<token>[\-a-zA-Z0-9]{1,64})$', api.CreditGroupRetrieveUpdateAPI.as_view()),

    url(r'^(?i)api/users/CreditUserScoresRetrieveUpdateAPI/(?P<token>[\-a-zA-Z0-9]{1,64})$', api.CreditUserScoresRetrieveUpdateAPI.as_view()),



]