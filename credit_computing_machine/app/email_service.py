from app.models import CreditGroup
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
    send_email_to_admin_credit_group(credit_group_id)


def send_invite_email_to_non_admin_credit_group(credit_group_id):
    credit_users = CreditGroup.objects.get_credit_non_admin_user(credit_group_id)

    for credit_user in credit_users:
        to_email, from_email, = credit_user.email, FROM_EMAIL
        template = 'invite_email'
        call_to_action = settings.FRONT_END_ROOT_URL + '/give_scores/' + '?token=' + credit_user.privateurl.token
        dict_context = {'name': credit_user.name,
                        'call_to_action': call_to_action
                        }
        send_email(to_email, from_email, template, dict_context)


def send_email_to_admin_credit_group(credit_group_id):
    credit_users = CreditGroup.objects.get_credit_admin_user(credit_group_id)
