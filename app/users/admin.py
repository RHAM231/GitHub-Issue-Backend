from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . forms import CustomUserCreationForm, CustomUserChangeForm
from . models import CustomUser, Profile


# Register the Profile model in our admin site
registeredModels = [
    Profile
]
admin.site.register(registeredModels)


# Customize our custom user admin interface
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'email', 'is_staff', 'is_active', 'is_guest',)
    list_filter = ('username', 'email', 'is_staff', 'is_active', 'is_guest',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_guest',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'password1', 'password2', 
                'is_staff', 'is_active', 'is_guest',
                )
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)

# Register our custom user classes
admin.site.register(CustomUser, CustomUserAdmin)
