from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from .models import CreditGroup, CreditUser, CreditScore
from .serializers import CreditGroupSerializer, CreditUserSerializer, CreditScoreSerializer

def manage_group(request,token):
    return render(request, 'app/group_manage.html', {
        'purl_id': token,
    })
def user_credit(request,token):
    return render(request, 'app/user_group_page.html', {
        'purl_id': token,
    })
