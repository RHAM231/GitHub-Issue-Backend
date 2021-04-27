from itertools import chain
from django.db.models import Q


def get_search_models(value):
    initial_models = ['list models here']
    model_names = [model.__name__ for model in initial_models]
    model_dict = dict(zip(model_names, initial_models))
    if value:
        for name in model_names:
            if value in model_names:
                search_models = [model_dict[value]]
            else:
                search_models = []
    else:
        search_models = initial_models
    return search_models


def get_search_results(form):
    search_models = get_search_models(form.cleaned_data['value'])
    field_names = list(form.cleaned_data.keys())
    lookups = []
    for model in search_models:
        fields = [x for x in model.meta.concrete_fields if x.name in field_names]

        foreign_key_fields = []
        fk_user_fields = []

        search_queries = []
        for field in fields:
            if (field.name in foreign_key_fields):
                search_text = "__name__icontains"
            elif (field.name in fk_user_fields):
                search_text = "__username__icontains"
            else:
                search_text = "__icontains"
            
            q_object = Q(**{field.name + search_text : form.cleaned_data[field.name]})

            search_queries.append(q_object)
        
        q_object = Q()
        for query in search_queries: