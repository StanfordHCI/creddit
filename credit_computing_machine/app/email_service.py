from app.models import CreditGroup , CreditUser
from post_office import mail
from django.conf import settings

FROM_EMAIL = 'abc@abc.com'


def send_email(to_email, from_email, template, dict_context):
    mail.send(
        to_email,  # List of email addresses also accepted
        from_email,
        template=template,  # Could be an EmailTemplate instance or name
        context=dict_context,
    )


def send_invite_email_to_all_credit_group(credit_group_id):
    send_invite_email_to_non_admin_credit_group(credit_group_id)
    send_manage_email_to_admin_credit_group(credit_group_id)


def send_invite_email_to_non_admin_credit_group(credit_group_id):
    credit_users = CreditGroup.objects.get_credit_non_admin_user(credit_group_id)
    credit_group = CreditGroup.objects.get(id=credit_group_id)

    credit_admin_users = CreditGroup.objects.get_credit_admin_user(credit_group_id)
    if credit_admin_users:
        admin_name = credit_admin_users[0].name
    else:
        admin_name= 'admin'

    for credit_user in credit_users:
        to_email, from_email, = credit_user.email, FROM_EMAIL
        template = 'invite_email'
        call_to_action = settings.FRONT_END_ROOT_URL + '/scores/'+ credit_user.privateurl.token
        dict_context = {'admin_name': admin_name,
                        'call_to_action': call_to_action,
                        'group_name':credit_group.name

                        }
        send_email(to_email, from_email, template, dict_context)


def send_manage_email_to_admin_credit_group(credit_group_id):
    credit_users = CreditGroup.objects.get_credit_admin_user(credit_group_id)
    credit_group = CreditGroup.objects.get(id=credit_group_id)
    for credit_user in credit_users:
        to_email, from_email, = credit_user.email, FROM_EMAIL
        template = 'manage_group_email'


        call_to_action = settings.FRONT_END_ROOT_URL + '/manage-group/'+credit_group.privateurl.token
        dict_context = {'name': credit_user.name,
                        'call_to_action': call_to_action,
                        'group_name': credit_group.name
                        }
        send_email(to_email, from_email, template, dict_context)


def send_score_updated_email_to_admin_credit_group(credit_group_id,credit_user_id):
    credit_admin_users = CreditGroup.objects.get_credit_admin_user(credit_group_id)
    credit_group = CreditGroup.objects.get(id=credit_group_id)
    name = CreditUser.objects.get(id = credit_user_id).name
    number_of_submitter = CreditUser.objects.filter(credit_group__id= credit_group_id,is_submitted=True).count()
    for credit_user in credit_admin_users:
        to_email, from_email, = credit_user.email, FROM_EMAIL
        template = 'updated_score_admin_email'
        call_to_action = settings.FRONT_END_ROOT_URL + '/manage-group/'+credit_group.privateurl.token
        dict_context = {'name': name,
                        'call_to_action': call_to_action,
                        'group_name': credit_group.name,
                        'number_of_submitter':number_of_submitter
                        }
        send_email(to_email, from_email, template, dict_context)
