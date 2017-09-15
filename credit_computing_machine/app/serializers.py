from django.db import IntegrityError
from rest_framework import serializers

from app import email_service
from credit_computing_machine.messages import validation_score_msg, validation_email_msg
from .models import CreditGroup
from .models import CreditUser
from .models import CreditScore
from .utility import Utility
from credit_computing_machine.drf_custom_exceptions import CustomAPIException

class CreditGroupCreateSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditGroup Create.
    '''

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditGroup
        fields = '__all__'
        read_only_fields = ['privateurl']


class CreditUserCreateSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditUser Create.
    '''

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditUser
        fields = '__all__'


class CreditUserSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditUser.
    '''

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditUser
        fields = '__all__'


class CreditGroupSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditGroup.
    '''
    credit_users = CreditUserSerializer(many=True)

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditGroup
        fields = ('id', 'name', 'credit_users')


class CreditScoreSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditUser Create.
    '''
    to_credit_user_name = serializers.ReadOnlyField()
    to_credit_user_email =  serializers.ReadOnlyField()
    class Meta:
        '''
        Serializer customization
        '''
        model = CreditScore

        fields = ('score','to_credit_user','from_credit_user','credit_group','to_credit_user_name','to_credit_user_email')
        extra_kwargs = {'to_credit_user': {'read_only': False}}

class CreditScoreUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditUser Create.
    '''

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditScore
        fields = ('score','to_credit_user','from_credit_user','credit_group')
        extra_kwargs = {'to_credit_user': {'read_only': True},'from_credit_user': {'read_only': True},'credit_group': {'read_only': True}}


class CreditUserUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditUser Create.
    '''

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditUser
        fields = ('name','email','score','is_admin','is_submitted','id')
        read_only_fields = ('is_admin','id',)
        # extra_kwargs = {'id': {'read_only': False}}

class CreditGroupUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditGroup Create.
    '''
    credit_users = CreditUserUpdateSerializer(many=True)
    class Meta:
        '''
        Serializer customization
        '''
        model = CreditGroup
        fields = ('name','credit_users')



class CreditUserScoreUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditGroup Create.
    '''
    from_credit_user = CreditScoreSerializer(many=True)
    group_name = serializers.CharField(source='credit_group.name',read_only=True)
    class Meta:
        '''
        Serializer customization
        '''
        model = CreditScore
        fields = ('from_credit_user','group_name')

    def update(self, instance, validated_data):
        credit_scores = validated_data.pop('from_credit_user')
        credit_score_serializer_data = CreditScoreSerializer(data=credit_scores, many=True)
        self.validate_scores(credit_scores)
        result = Utility.save_and_update_data(CreditScoreUpdateSerializer,credit_scores,CreditScore,['from_credit_user','to_credit_user', 'credit_group'])
        return instance

    def validate_scores(self,credit_scores):
        score = 0
        TOTAL_MAX_SCORE = 100
        for credit_score in credit_scores:
            score = score + credit_score.get('score',0)

        if (score > TOTAL_MAX_SCORE):
            raise CustomAPIException({'scores': validation_score_msg})