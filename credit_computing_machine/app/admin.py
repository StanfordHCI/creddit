from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.apps import apps

from app.models import CreditUser

# app = apps.get_app_config('app')
#
# for model_name, model in app.models.items():
#     admin.site.register(model)

class CreditUserAdmin(admin.ModelAdmin):
    list_display = CreditUser._meta.get_all_field_names()
admin.site.register(CreditUser, CreditUserAdmin)