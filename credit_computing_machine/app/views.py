from django.shortcuts import render

# Create your views here.
from django.dispatch import receiver
from privateurl.signals import privateurl_ok, privateurl_fail

@receiver(privateurl_ok)
def conf(request, obj, action, **kwargs):
    import pdb
    pdb.set_trace()
    if action != 'conf':
        return

