from datetime import date

from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


def check_date_not_past(value: date):
    if value < date.today():
        raise ValidationError(
            '%(value)s is in the past',
            params={'value': value},
        )


class Vacancy(models.Model):
    STATUS = [("draft", "Черновик"), ("open", "Открыта"), ("closed", "Closed")]

    slug = models.SlugField(max_length=50, validators=[MinLengthValidator(3)])
    text = models.CharField(max_length=1000)
    status = models.CharField(max_length=10, choices=STATUS, default="draft")
    created = models.DateField(auto_now_add=True, validators=[check_date_not_past])
