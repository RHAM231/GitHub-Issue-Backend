from django.db import models
from django.contrib.auth.models import AbstractUser


# Let's create a custom user class to allow us to easily customize our users in the
# the future if we want to
class CustomUser(AbstractUser):
    is_guest = models.BooleanField('guest_status', default=False)

    def __str__(self):
        return self.username


# Let's a create a profile model with a one to one relation with user.
# This is where we'll set name and image.
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