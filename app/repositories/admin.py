from django.contrib import admin
from . models import (
    Repository, RepoFolder, RepoFile, LineOfCode
)


registeredModels = [
    Repository, RepoFolder, RepoFile, LineOfCode
]
admin.site.register(registeredModels)