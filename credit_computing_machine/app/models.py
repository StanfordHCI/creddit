from django.db import models
from credit_computing_machine.models import TimestampModel
# Create your models here.


class CreditGroup(TimestampModel):
    name = models.CharField(max_length=200)


class CreditUser(TimestampModel):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    credit_group = models.ForeignKey(CreditGroup)


class CreditScore(TimestampModel):
    score = models.FloatField()
    from_credit_user = models.ForeignKey(CreditUser)
    to_credit_user = models.ForeignKey(CreditUser)
    credit_group = models.ForeignKey(CreditGroup)

