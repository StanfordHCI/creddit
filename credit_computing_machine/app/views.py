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

# def manage_group(request,purl_id):
#     credit_group = CreditGroup.objects.filter(privateurl__id=purl_id).first()
#     response = CreditGroupSerializer(credit_group).data
#     return HttpResponse(str(response))
#
# def user_credit(request,purl_id):
#     credit_user = CreditUser.objects.filter(privateurl__id=purl_id).first()
#     credit_group = credit_user.credit_group
#     credit_users = CreditUser.objects.filter(credit_group = credit_group)
#     response = {'credit_users': CreditUserSerializer(credit_users, many=True).data}
#     credit_scores = CreditScore.objects.filter(from_credit_user=credit_user)
#     response['credit_scores'] = CreditScoreSerializer(credit_scores,many=True).data
#     response['credit_user'] = CreditUserSerializer(credit_user).data
#     return HttpResponse(str(response))