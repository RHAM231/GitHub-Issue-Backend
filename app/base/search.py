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



    # model_names = [model.__name__ for model in initial_models]
    # model_dict = dict(zip(model_names, initial_models))
    # if value:
    #     for name in model_names:
    #         if value in model_names:
    #             search_models = [model_dict[value]]
    #         else:
    #             search_models = []
    # else:
    #     search_models = initial_models
    # return search_models


def get_search_results(form):
    modules = [repo_models, issue_models]
    search_models = get_search_models(modules)
    lookups = []

    # Define a list of fields we want to search by
    field_names = ['name', 'title', 'state', 'body']
    for model in search_models:
        fields = [x for x in model._meta.get_fields() if x.name in field_names]

        search_queries = []
        for field in fields:
            search_text = "__icontains"
            q_object = Q(**{field.name + search_text : form.cleaned_data['master_search']})
            search_queries.append(q_object)
        
        q_object = Q()
        for query in search_queries:
            # Use '|' for OR and '&' for AND.
            q_object = q_object & query
        
        results = model.objects.filter(q_object)
        lookups.append(results)
    print()
    print(lookups)
    print()

    # # add created_at field to other objects besides issues
    # results_list = sorted(chain.from_iterable(lookups), key=lambda instance: instance.created_at)
    # return results_list