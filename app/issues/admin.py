from django.contrib import admin
from . models import (
    Issue
)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    readonly_fields = ('stamp',)
