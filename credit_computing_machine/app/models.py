from django.db import models
from credit_computing_machine.models import TimestampModel


# Create your models here.

class CreditGroupManager(models.Manager):

    def get_credit_all_user(self, credit_group_id):
        return CreditUser.objects.filter(credit_group=credit_group_id)

    def get_credit_admin_user(self, credit_group_id):
        return CreditUser.objects.filter(credit_group=credit_group_id, is_admin=True)

    def get_credit_non_admin_user(self, credit_group_id):
        return CreditUser.objects.filter(credit_group=credit_group_id, is_admin=False)


class CreditGroup(TimestampModel):
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    objects = CreditGroupManager()


class CreditUser(TimestampModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    credit_group = models.ForeignKey(CreditGroup, null=True, blank=True)
    is_admin = models.BooleanField(default=False)


class CreditScore(TimestampModel):
    score = models.FloatField()
    from_credit_user = models.ForeignKey(
        CreditUser, related_name='from_credit_user')
    to_credit_user = models.ForeignKey(
        CreditUser, related_name='to_credit_user')
    credit_group = models.ForeignKey(CreditGroup)
