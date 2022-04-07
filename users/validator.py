import re 

from .views import ValidationError

REGEX_USER     = '^[a-z0-9+]{3,15}$'
REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

def validate_signup(user, password):
    if not re.match(REGEX_USER, user):
        raise ValidationError('INVALID_ID')

    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError('INVALID_PASSWORD')
