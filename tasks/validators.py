from django.core.exceptions import ValidationError
from django.utils.timezone import now


def validate_deadline_in_future(value):
    if value <= now():
        raise ValidationError('Deadline must be in the future.')