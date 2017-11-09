from django.db import models
from credit_computing_machine.models import TimestampModel
from privateurl.models import PrivateUrl
from django.db.models.signals import pre_save
from django.dispatch import receiver
# Create your models here.

class CreditManager(models.Manager):

    def get_credit_all_user(self, credit_group_id):
        return CreditUser.objects.filter(credit_group=credit_group_id)

    def get_credit_admin_user(self, credit_group_id):
        return CreditUser.objects.filter(credit_group=credit_group_id, is_admin=True)

    def get_credit_non_admin_user(self, credit_group_id):
        return CreditUser.objects.filter(credit_group=credit_group_id, is_admin=False)

    def get_dict_scores(self,credit_group_id):
        users = CreditGroup.objects.get_credit_non_admin_user(credit_group_id).filter(is_diclined=False)
        credit_scores = CreditScore.objects.filter(credit_group_id=credit_group_id)
        dict_scores = {}
        for user in users:
          dict_scores[user.email] = {}
          user_scores = credit_scores.filter(from_credit_user = user)
          for user_score in user_scores:
            dict_scores[user.email][user_score.to_credit_user.email] = user_score.score

        return dict_scores


class CreditGroup(TimestampModel):
    name = models.CharField(max_length=200)
    is_deleted = models.BooleanField(default=False)
    privateurl = models.ForeignKey(PrivateUrl,null=True)
    objects = CreditManager()

    def __str__(self):
        return self.name

@receiver(pre_save, sender=CreditGroup, dispatch_uid="add_group_purl")
def add_group_purl(sender, instance, **kwargs):
    if not instance.privateurl:
        purl = PrivateUrl.create('manage_credit_score')
        instance.privateurl= purl

class CreditUser(TimestampModel):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    score = models.FloatField(default=0)
    credit_group = models.ForeignKey(CreditGroup, null=True, blank=True, related_name='credit_users')
    is_admin = models.BooleanField(default=False)
    privateurl = models.ForeignKey(PrivateUrl, null=True)
    is_submitted = models.BooleanField(default=False)
    is_diclined = models.BooleanField(default=False)
    objects = CreditManager()


    def __str__(self):
        return '%s from %s'%(self.name,self.credit_group)

    class Meta:
        unique_together = ('credit_group', 'email','is_admin')

@receiver(pre_save, sender=CreditUser, dispatch_uid="add_user_purl")
def add_user_purl(sender, instance, **kwargs):
    if not instance.privateurl:
        purl = PrivateUrl.create('user_credit')
        instance.privateurl= purl


class CreditScore(TimestampModel):
    score = models.FloatField()
    from_credit_user = models.ForeignKey(
        CreditUser, related_name='from_credit_user')
    to_credit_user = models.ForeignKey(
        CreditUser, related_name='to_credit_user')
    credit_group = models.ForeignKey(CreditGroup)
    objects = CreditManager()

    @property
    def to_credit_user_name(self):
        return self.to_credit_user.name

    @property
    def to_credit_user_email(self):
        return self.to_credit_user.email

    def __str__(self):
        return '%s to %s from %s'%(self.from_credit_user,self.to_credit_user,self.credit_group)
