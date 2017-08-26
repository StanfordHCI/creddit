from django.core.exceptions import ObjectDoesNotExist
from .models import CreditGroup

class Utility:
    '''
    Gernral Utility class for common functions
    '''
    @staticmethod
    def send_welcome_email_to_all_credit_group(credit_group_id):
        Utility.send_email_to_non_admin_credit_group(credit_group_id)
        Utility.send_email_to_admin_admin_credit_group(credit_group_id)

    @staticmethod
    def send_welcome_email_to_non_admin_credit_group(credit_group_id):
        credit_users = CreditGroup.objects.get_credit_non_admin_user(credit_group_id)

    @staticmethod
    def send_welcome_email_to_admin_admin_credit_group(credit_group_id):
        credit_users = CreditGroup.objects.get_credit_admin_user(credit_group_id)

    @staticmethod
    def get_model(data, model, db_key=None, data_key=None):
        if (db_key and data_key):
            try:
                kw = {db_key: data[data_key]}
                obj_model = model.objects.get(**kw)
            except ObjectDoesNotExist:
                obj_model = None
        else:
            obj_model = None

        return obj_model

    @staticmethod
    def save_and_update_data(serializer,
                             lst_data, model,
                             db_keys=None, id='id'):
        '''
        create or update the object according
        to specified serializer and model

        KeyWords Arguments

        serializer  -- Serializer for which you want to validate and save
        lst_data    -- data to be saved
        model       -- model in which data need to be saved
        update_keys      -- db key in model (used for update)
        id          -- primary key for database
        '''
        count_update = 0
        count_save = 0
        lst_errors = []
        for data in lst_data:
            if(db_keys):
                try:
                    kw={}
                    for item in db_keys:
                        kw[item]=data[item]
                    print(kw)
                    obj_model = model.objects.get(**kw)
                except ObjectDoesNotExist:
                    obj_model = None
            else:
                obj_model = None

            if not obj_model:
                # Perform creations.
                serialize_data = serializer(
                    data=data)
                if serialize_data.is_valid():
                    serialize_data.save()
                    count_save = count_save + 1
                else:
                    lst_errors.append(serialize_data.errors)

            else:
                # Perform updations.
                serialize_data = serializer(obj_model,
                                            data=data, partial=True)
                if serialize_data.is_valid():
                    count_update = count_update + 1
                    serialize_data.save()
                else:
                    lst_errors.append(serialize_data.errors)
        return {'count_save': count_save,
                'count_update': count_update,
                'lst_errors': lst_errors}