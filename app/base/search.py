from itertools import chain
from django.db.models import Q

from repositories import models as repo_models
from issues import models as issue_models


def get_search_models(modules):
    search_models = []
    for module in modules:
        model_classes = dict([(name, cls) for name, cls in module.__dict__.items() if isinstance(cls, type)])
        filter_classes = ('CustomUser', 'LineOfCode', 'TestIssue')
        for key in filter_classes:
            model_classes.pop(key, None)
        models = list(model_classes.values())
        search_models = list(set(search_models + models))
    return search_models


def get_search_results(form):
    modules = [repo_models, issue_models]
    # search_models = get_search_models(modules)
    search_models = [issue_models.Issue, repo_models.Repository]
    lookups = []

    # Define a list of fields we want to search by
    field_names = ['name', 'title', 'state', 'body']
    for model in search_models:
        fields = [x for x in model._meta.get_fields() if x.name in field_names]
        print()
        print(fields)
        print()

        search_queries = []
        for field in fields:
            search_text = "__icontains"
            q_object = Q(**{field.name + search_text : form.cleaned_data['master_search']})
            search_queries.append(q_object)
        print()
        print(search_queries)
        print()
        
        q_object = Q()
        for query in search_queries:
            # Use '|' for OR and '&' for AND.
            q_object = q_object & query
        
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

