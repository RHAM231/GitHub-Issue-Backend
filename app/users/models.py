from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_guest = models.BooleanField('guest_status', default=False)

    def __str__(self):
        return self.username

