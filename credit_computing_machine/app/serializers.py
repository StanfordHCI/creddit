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


class CreditScoreSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditUser Create.
    '''

    class Meta:
        '''
        Serializer customization
        '''
        model = CreditScore
        fields = '__all__'

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
        # for credit_user in credit_users:
        #     pass
        #     name = credit_user.get('name')
        #     ToDO save and update credit_users according to emails ; as emails cannot be changed
        return instance


class CreditUserScoreUpdateSerializer(serializers.ModelSerializer):
    '''
    Serializer for CreditGroup Create.
    '''
    from_credit_user = CreditScoreSerializer(many=True)
    class Meta:
        '''
        Serializer customization
        '''
        model = CreditScore
        fields = ('from_credit_user',)

    def update(self, instance, validated_data):
        credit_users = validated_data.pop('credit_user_scores')
        #     ToDO save and update credit_user_scores according to emails
        return instance