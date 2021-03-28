from django.contrib import admin
from . models import (
    Issue, TestIssue
)

registeredModels = [
    Issue, TestIssue
]
admin.site.register(registeredModels)
