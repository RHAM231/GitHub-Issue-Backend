from django.contrib import admin
from . models import (
    Issue, TestIssue
)

registeredModels = [
    # Issue, 
    TestIssue
]
admin.site.register(registeredModels)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    # fields = ('title', 'state')
    # fieldsets = (
    #     (None, {
    #         'fields': ('title', 'state')
    #     })
    # )
    readonly_fields = ('stamp',)
