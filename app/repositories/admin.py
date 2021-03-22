from django.contrib import admin
from . models import (
    Repository, RepoFolder, RepoFile
)

registeredModels = [
    Repository, RepoFolder, RepoFile
]
admin.site.register(registeredModels)