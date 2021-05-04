from django.contrib import admin
from . models import (
    Issue
)


# Use custom registration to make the stamp field read-only
@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    readonly_fields = ('stamp',)
