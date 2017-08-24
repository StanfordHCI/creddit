import copy
from django.conf import settings

from rest_framework import generics, status
from django.contrib.auth import authenticate

from app.models import CreditGroup, CreditScore,CreditUser
from .serializers import CreditGroupCreateSerializer
from .serializers import CreditUserCreateSerializer ,CreditGroupUpdateSerializer,CreditUserScoreUpdateSerializer
from privateurl.models import PrivateUrl
from rest_framework.response import Response


class CreditGroupCreateApi(generics.CreateAPIView):
    serializer_class = CreditGroupCreateSerializer

    def create(self, request, *args, **kwargs):
        response = {'status':'ok'}
        request_data = copy.deepcopy(request.data)

        credit_users = request_data.get('credit_users')
        credit_user_serializer_data = CreditUserCreateSerializer(data=credit_users,many=True)
        request_data.pop('credit_users')
        credit_group_serializer_data = CreditGroupCreateSerializer(data=request_data)
        if credit_group_serializer_data.is_valid():
            if credit_user_serializer_data.is_valid():
                credit_group = credit_group_serializer_data.save()

                for credit_user in credit_users:
                    credit_user['credit_group']= credit_group.id
                credit_user_serializer_data = CreditUserCreateSerializer(data=credit_users, many=True)
                if credit_user_serializer_data.is_valid():
                    credit_users = credit_user_serializer_data.save()
                    print(credit_users)
                    user_ids = [i.id for i in credit_users]
                    for index,user_id in  enumerate(user_ids):
                        for internal_index, internal_user_id in enumerate(user_ids):
                            if user_id != internal_user_id:
                                CreditScore.objects.create(from_credit_user_id= user_id,to_credit_user_id =internal_user_id,credit_group= credit_group ,score = 0)
            else:
                pass
                #return credit_user_serializer_data.errors
        else:
            pass
            #return credit_group_serializer_data.errors

        return Response(response, status=status.HTTP_200_OK)

class CreditGroupRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CreditGroupUpdateSerializer

    def get_object(self):
        return CreditGroup.objects.get(privateurl__token__exact=self.kwargs['token'])

# def manage_group(request,purl_id):
#     credit_group = CreditGroup.objects.filter(privateurl__id=purl_id).first()
#     response = CreditGroupSerializer(credit_group).data
#     return HttpResponse(str(response))


class CreditUserScoresRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CreditUserScoreUpdateSerializer

    def get_object(self):
        return CreditUser.objects.get(privateurl__token__exact=self.kwargs['token'])


