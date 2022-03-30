import json
import re 

from .views import ValidationError

REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'

def validate_password(password):
    if not re.match(REGEX_PASSWORD, password):
        raise ValidationError('INVALID_PASSWORD')
