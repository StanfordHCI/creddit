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