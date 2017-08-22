from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
import datetime
from .models import CreditGroup
def manage_group(request,purl_id):
    credit_group = CreditGroup.objects.filter(privateurl__id=purl_id).first()
    print(CreditGroup.objects.get_credit_all_user(credit_group.id))
    html = "<html><body>It is now </body></html>"
    return HttpResponse(html)