from datetime import datetime

from django.utils.timezone import now
from django.core.exceptions import ValidationError


def validate_deadline_in_future(value: datetime):
    if value <= now():
        raise ValidationError("Deadline must be in the future.")
