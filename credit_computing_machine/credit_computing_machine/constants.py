EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'duahimanshu101@gmail.com'
EMAIL_HOST_PASSWORD = 'clasmate'


FRONT_END_ROOT_URL = 'http://18.220.171.98:8080'
EMAIL_BACKEND = 'post_office.EmailBackend'

# Put this in settings.py
POST_OFFICE = {
    'BATCH_SIZE': 50
}
