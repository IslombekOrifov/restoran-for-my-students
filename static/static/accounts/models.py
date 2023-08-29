from django.db import models
from django.contrib.auth.models import AbstractUser, User

from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

from .validators import validate_phone, validate_image
from .services import upload_avatar_path

class CustomUser(AbstractUser):
    """ Custom user model """
    email = models.EmailField(blank=True)
    phone = models.CharField(
        max_length=13, 
        blank=True, 
        validators=[validate_phone]
    )

    REQUIRED_FIELDS = []

    first_login = models.DateField(null=True)
    middle_name = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(
        upload_to=upload_avatar_path, 
        validators=[validate_image], 
        blank=True, null=True
    )
    is_deleted = models.BooleanField(default=False)


    def __str__(self):
        if self.get_full_name():
            return f"{self.get_full_name()}"
        return f'{self.email} > {self.username}'

    def save(self, *args, **kwargs):
        self.username = ' '.join(self.username.strip().split())
        self.email = ' '.join(self.email.strip().split())
        self.phone = ' '.join(self.phone.strip().split())
        super().save(*args, **kwargs)

