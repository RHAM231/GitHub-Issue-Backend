from django.contrib import admin
from . models import (
    Issue
)

registeredModels = [
    Issue
]
admin.site.register(Issue)
