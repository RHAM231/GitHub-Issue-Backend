from itertools import chain
from django.db.models import Q


def get_search_models():
    initial_models = ['list models here']
    model_names = [model.__name__ for model in initial_models]
    model_dict = dict(zip(model_names, initial_models))