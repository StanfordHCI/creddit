from rest_framework import serializers
from .models import CreditGroup
from .models import CreditUser
from .models import CreditScore


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
    Serializer for CreditUser Create.
    '''

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditUser
        fields = '__all__'

class CreditGroupSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditGroup Create.
    '''
    credit_users = CreditUserSerializer(many=True)

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditGroup
        fields = ('id', 'name', 'credit_users')



