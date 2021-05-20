from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    is_guest = models.BooleanField('guest_status', default=False)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    image = models.ImageField(default='static/images/logo.jpg', upload_to='images')

    def save(self, *args, **kwargs):
        if self.user.username == 'admin':
            self.name = 'Rex Mitchell'
        else:
            self.name = self.user.username
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.user.username} Profile'
