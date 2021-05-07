from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from . models import CustomUser


# Rewrite the basic user forms, since we're using a custom user model
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')