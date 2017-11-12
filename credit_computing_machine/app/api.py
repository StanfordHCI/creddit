import copy
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import generics, status
from django.contrib.auth import authenticate

from app.models import CreditGroup, CreditScore, CreditUser
from credit_computing_machine.messages import validation_email_msg
from .serializers import CreditGroupCreateSerializer , CreditScoreSerializer, CreditUserSerializer
from .serializers import CreditUserCreateSerializer, CreditGroupUpdateSerializer, CreditUserScoreUpdateSerializer
from privateurl.models import PrivateUrl
from rest_framework.response import Response
from . import email_service
from credit_computing_machine.drf_custom_exceptions import CustomAPIException
from django.db import transaction
from django.db import IntegrityError
from computing_machine import compute_scores


class CreditGroupCreateApi(generics.CreateAPIView):
    serializer_class = CreditGroupCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """
        Create the group
        :param request:
        :param args:
        :param kwargs:
        :return: response
        """
        response = {}
        request_data = copy.deepcopy(request.data)

        credit_users = request_data.get('credit_users')
        credit_admin_users = request_data.get('credit_admin')
        request_data.pop('credit_users')
        request_data.pop('credit_admin')
        credit_group_serializer_data = CreditGroupCreateSerializer(data=request_data)
        if credit_group_serializer_data.is_valid():
            credit_group = credit_group_serializer_data.save()
            for credit_user in credit_users:
                credit_user['credit_group'] = credit_group.id
            for credit_user in credit_admin_users:
                credit_user['credit_group'] = credit_group.id
                credit_user['is_admin'] = True
            credit_user_serializer_data = CreditUserCreateSerializer(data=credit_users, many=True)
            credit_admin_user_serializer_data = CreditUserCreateSerializer(data=credit_admin_users, many=True)
            if credit_admin_user_serializer_data.is_valid():
                if credit_user_serializer_data.is_valid():
                    try:
                        credit_admin_users = credit_admin_user_serializer_data.save()
                        credit_users = credit_user_serializer_data.save()
                    except IntegrityError as e:
                        raise CustomAPIException({'email': validation_email_msg})

                    user_ids = [i.id for i in credit_users]
                    for index, user_id in enumerate(user_ids):
                        for internal_index, internal_user_id in enumerate(user_ids):
                            # if user_id != internal_user_id:
                            CreditScore.objects.create(from_credit_user_id=user_id,
                                                       to_credit_user_id=internal_user_id,
                                                       credit_group=credit_group, score=0)

                    email_service.send_invite_email_to_all_credit_group(credit_group.id)

                    response = {'msg': 'Group created', 'token': credit_group.privateurl.token}
                else:
                    raise CustomAPIException(credit_user_serializer_data.errors)
            else:
                raise CustomAPIException(credit_admin_user_serializer_data.errors)
        else:
            raise CustomAPIException(credit_group_serializer_data.errors)

        return Response(response, status=status.HTTP_200_OK)


class CreditGroupRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CreditGroupUpdateSerializer

    def get_object(self):
        try:
            return CreditGroup.objects.get(privateurl__token__exact=self.kwargs['token'])
        except CreditGroup.DoesNotExist:
            raise CustomAPIException('Not a vaild page')

    def update(self, request, *args, **kwargs):
        instance = CreditGroup.objects.get(name=request.data.get('name'))
        credit_group = instance
        credit_users = request.data.pop('credit_users')
        ids = []
        for item in credit_users:
            if item.get('id'):
                ids.append(int(item.get('id')))
        CreditUser.objects.filter(is_admin=False).exclude(id__in=ids).delete()
        only_new_credit_users = []
        for item in credit_users:
            if not item.get('id'):
                item['credit_group'] = instance.id
                only_new_credit_users.append(item)

        credit_user_serializer_data = CreditUserCreateSerializer(data=only_new_credit_users, many=True)
        if credit_user_serializer_data.is_valid():
            try:
                credit_users = credit_user_serializer_data.save()
            except IntegrityError as e:
                raise CustomAPIException({'email': validation_email_msg})

            user_ids = [i.id for i in credit_users]
            for index, user_id in enumerate(user_ids):
                for internal_index, internal_user_id in enumerate(user_ids):
                    # if user_id != internal_user_id:
                    CreditScore.objects.create(from_credit_user_id=user_id,
                                               to_credit_user_id=internal_user_id,
                                               credit_group=credit_group, score=0)

            email_service.send_invite_email_to_all_credit_group(credit_group.id)

            response = {'msg': 'Group updated', 'token': credit_group.privateurl.token}
        else:
            raise CustomAPIException(credit_user_serializer_data.errors)

        return Response(response, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """
        To retrive the Group details via token in kwargs
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = serializer.data
        credit_users = result.get('credit_users')
        credit_users = [credit_user for credit_user in credit_users if not credit_user.get('is_admin')]
        credit_admin_users = []

        if instance:
            credit_admin_users = CreditUser.objects.filter(credit_group= instance,is_admin=True)
        if credit_users:
            credit_group = self.get_object()
            dict_scores = CreditGroup.objects.get_dict_scores(credit_group.id)
            compute_result = compute_scores(dict_scores)

            for credit_user in credit_users:
                email = credit_user.get('email')
                # if not credit_user.get('is_submitted'):
                #     credit_user['score'] = 0
                #     continue
                if email and compute_result.get(email):
                    credit_user['score'] = compute_result.get(email)
                if credit_admin_users and email:
                    if credit_admin_users[0].email == email:
                        credit_user['is_admin'] = True
                        credit_user['privateurl'] = CreditUser.objects.filter(id=credit_user.get('id'))[0].privateurl.token

        result['credit_users'] = credit_users
        return Response(result)

class CreditUserScoresRetrieveUpdateAPI(generics.RetrieveUpdateAPIView):
    serializer_class = CreditUserScoreUpdateSerializer

    def get_object(self):
        try:
            return CreditUser.objects.get(privateurl__token__exact=self.kwargs['token'])
        except CreditUser.DoesNotExist:
            raise CustomAPIException('Not a vaild page')

    def put(self, request, *args, **kwargs):
        """
        Edit and assign the score to creddit users
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        if not (request.data.get('is_declined')):
            updated_result = self.update(request, *args, **kwargs)
        else:
            updated_result = Response({'detail':'declined successfull'})
        instance = self.get_object()
        instance.is_submitted = True
        instance.is_declined = bool (request.data.get('is_declined'))
        instance.save()
        email_service.send_score_updated_email_to_admin_credit_group(instance.credit_group.id, instance.id)
        return updated_result

    def retrieve(self, request, *args, **kwargs):
        """
        Only retrive the scores of different creddit users in the group
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = serializer.data
        token = kwargs.get('token')
        if token:
            self_user = CreditUser.objects.filter(privateurl__token__exact=token).first()
            result['self_user'] = CreditUserSerializer(self_user).data
            
        credit_admin_users = CreditGroup.objects.get_credit_admin_user(instance.credit_group.id)
        if credit_admin_users:
            result['admin_user'] = CreditUserSerializer(credit_admin_users[0]).data

        return Response(result)


class CreditGroupCount(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        number_of_groups = CreditGroup.objects.all().count()
        return Response({'number_of_groups':number_of_groups})


class CreditGroupInviteEmail(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        credit_user_id = int(request.query_params.get('id'))
        try:
            credit_user = CreditUser.objects.get(id= credit_user_id)
        except ObjectDoesNotExist:
            raise CustomAPIException({'email': 'User not exist'})
        credit_group = credit_user.credit_group

        credit_admin_users = CreditGroup.objects.get_credit_admin_user(credit_group.id)
        if credit_admin_users:
            admin_name = credit_admin_users[0].name
        else:
            admin_name = 'admin'
        email_service.send_invite_email(credit_user,admin_name, credit_group)
        return Response({'sent':'ok'})