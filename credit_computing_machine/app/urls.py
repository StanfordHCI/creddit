from django.conf.urls import url
from . import api


urlpatterns = [
    url(r'^(?i)api/CreditGroupCreateApi/', api.CreditGroupCreateApi.as_view()),

]