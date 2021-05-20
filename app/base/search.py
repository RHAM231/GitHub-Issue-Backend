from itertools import chain
from django.db.models import Q
from django.conf import settings
from issues import models as issue_models
from repositories import models as repo_models


def get_search_models(modules, exclusions):
    search_models = []
    for module in modules:
        model_classes = dict([(name, cls) for name, cls in module.__dict__.items() if isinstance(cls, type)])
        for key in exclusions:
            model_classes.pop(key, None)
        models = list(model_classes.values())
        search_models = list(set(search_models + models))
    return search_models


def get_search_results(form):
    db_engine = settings.DATABASES['default']['ENGINE']
    modules = [repo_models, issue_models]
    exclusions = ('CustomUser', 'LineOfCode', 'TestIssue', 'Profile')
    search_models = get_search_models(modules, exclusions)
    lookups = []

    field_names = ['name', 'title', 'state', 'body']
    for model in search_models:
        fields = [x for x in model._meta.get_fields() if x.name in field_names]

        search_queries = []
        for field in fields:
            if db_engine == 'django.db.backends.sqlite3':
                search_text = "__icontains"
            elif db_engine == 'django.db.backends.postgresql':
                search_text = "__search"

            q_object = Q(**{field.name + search_text : form.cleaned_data['master_search']})
            search_queries.append(q_object)
        
        q_object = Q()
        for query in search_queries:
            q_object = q_object | query
        
        results = model.objects.filter(q_object)
        lookups.append(results)

    results_list = sorted(chain.from_iterable(lookups), key=lambda instance: instance.created_at)
    return results_list


def get_structured_search_results(form):
    results_list = get_search_results(form)

    issues, repos, folders, files = [], [], [], []
    for model_object in results_list:
        if model_object.__class__.__name__ == 'Issue':
            issues.append(model_object)
        elif model_object.__class__.__name__ == 'Repository':
            repos.append(model_object)
        elif model_object.__class__.__name__ == 'RepoFolder':
            folders.append(model_object)
        elif model_object.__class__.__name__ == 'RepoFile':
            files.append(model_object)
    return(issues, repos, folders, files)
