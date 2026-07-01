"""
Custom validators used across the Course Management API models and serializers.
"""

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


# Validates phone numbers: optional leading +, 7 to 15 digits.
phone_validator = RegexValidator(
    regex=r"^\+?\d{7,15}$",
    message="Enter a valid phone number (7-15 digits, optional leading '+').",
)

# Validates course codes: 2-4 uppercase letters followed by 2-4 digits, e.g. CS101, MATH2001.
course_code_validator = RegexValidator(
    regex=r"^[A-Z]{2,4}\d{2,4}$",
    message="Course code must be 2-4 uppercase letters followed by 2-4 digits (e.g. CS101).",
)


def validate_credits(value):
    """Ensure course credits fall within an acceptable academic range."""
    if value < 1 or value > 10:
        raise ValidationError(f"{value} is not a valid credit value. Credits must be between 1 and 10.")


def validate_name(value):
    """Ensure a name field contains only letters, spaces, hyphens, and apostrophes."""
    if not re.match(r"^[A-Za-z\s\.\-']+$", value):
        raise ValidationError(
            "Name may only contain letters, spaces, periods, hyphens, and apostrophes."
        )
