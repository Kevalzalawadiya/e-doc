from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class AdminUser(AbstractUser):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    mobile_number = models.CharField(
        validators=[phoneNumberRegex],
        max_length=10,
        unique=True,
        help_text="Enter your 10 digit contect number. ",
    )
    address = models.TextField(
        null=True, blank=True, help_text="Enter your store address."
    )
    is_superuser = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    forget_password_token = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.username


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    def delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True