from django.contrib import admin
from . models import (
    Repository, RepoFolder, RepoFile, LineOfCode
)

# Register our models in the admin site
registeredModels = [
    Repository, RepoFolder, RepoFile, LineOfCode
]
admin.site.register(registeredModels)