from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.apps import apps

from app.models import CreditUser, CreditScore


# app = apps.get_app_config('app')
#
# for model_name, model in app.models.items():
#     admin.site.register(model)

class CreditUserAdmin(admin.ModelAdmin):
    list_display = ('name','email','credit_group')
admin.site.register(CreditUser, CreditUserAdmin)

class CreditScoreAdmin(admin.ModelAdmin):
    list_display = ('from_credit_user','to_credit_user','score','credit_group')
admin.site.register(CreditScore, CreditScoreAdmin)