from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import CreditGroup
from .serializers import CreditGroupSerializer
def manage_group(request,purl_id):
    credit_group = CreditGroup.objects.filter(privateurl__id=purl_id).first()
    credit_group = CreditGroup.objects.filter(privateurl__id=purl_id).first()
    response = CreditGroupSerializer(credit_group).data
    return HttpResponse(str(response))