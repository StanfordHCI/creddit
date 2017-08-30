from rest_framework.exceptions import ParseError

class CustomAPIException(ParseError):
    status_code = 400
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'