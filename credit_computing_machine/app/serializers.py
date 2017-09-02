from rest_framework import serializers
from .models import CreditGroup
from .models import CreditUser
from .models import CreditScore
from .utility import Utility

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


class CreditScoreSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditUser Create.
    '''
    to_credit_user_name = serializers.ReadOnlyField()
    class Meta:
        '''
        Serializer customization
        '''
        model = CreditScore

        fields = ('score','to_credit_user','from_credit_user','credit_group','to_credit_user_name')
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
        fields = ('name','email')

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

    def update(self, instance, validated_data):
        credit_users = validated_data.pop('credit_users')
        instance.name = validated_data['name']
        instance.save()
        credit_group_serializer_data = CreditUserUpdateSerializer(data=credit_users, many=True)
        if credit_group_serializer_data.is_valid():
            for item in credit_users:
                item['credit_group'] = instance.id
            result = Utility.save_and_update_data(CreditUserUpdateSerializer,credit_users,CreditUser,['email','credit_group'])
        return instance


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
        result = Utility.save_and_update_data(CreditScoreUpdateSerializer,credit_scores,CreditScore,['from_credit_user','to_credit_user', 'credit_group'])
        return instance