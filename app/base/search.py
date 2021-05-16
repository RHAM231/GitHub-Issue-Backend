# Python Imports
from itertools import chain

# Django Imports: Logic from the Django Framework
from django.db.models import Q
from django.conf import settings

# Django Imports: Logic specific to this project
from issues import models as issue_models
from repositories import models as repo_models


#################################################################################################################################
# SUMMARY
#################################################################################################################################

'''
Let's build basic search functionality for our site (master search bar in the navbar). We define a get_search_models() method to
dynamically extract our searchable classes, excluding the ones we don't want.

Next we build a get_search_results() method. This queries our list of search models by the term provided from our search form and
returns a sorted list of results from the database.

Last we define a get_structured_search_results() method called by the SearchResultsView in base.views.py. This takes our
sorted list and breaks it into lists by model, returning the lists to the SearchResultsView.
'''

#################################################################################################################################
# BEGIN CODE
#################################################################################################################################


# Method for dynamically importing our models. We pass it a list of modules to iterate over and a list of classes to exclude.
# Returns a list of search models to construct queries from.
def get_search_models(modules, exclusions):
    search_models = []
    for module in modules:
        # Get our models from each module as a dictionary in case we need a dictionary structure in the future
        model_classes = dict([(name, cls) for name, cls in module.__dict__.items() if isinstance(cls, type)])
        # Remove the classes we wish to exclude
        for key in exclusions:
            model_classes.pop(key, None)
        # Convert our dictionary to a list for now and filter out duplicates
        models = list(model_classes.values())
        search_models = list(set(search_models + models))
    return search_models


# Given a form from our search view, return a query list based on our search term in our navbar search field
def get_search_results(form):
    # Go to our settings file and retrieve our database type
    db_engine = settings.DATABASES['default']['ENGINE']
    # Define our modules and exclusions so we can pass them to our get_search_models method above
    modules = [repo_models, issue_models]
    exclusions = ('CustomUser', 'LineOfCode', 'TestIssue', 'Profile')
    # Get our search models
    search_models = get_search_models(modules, exclusions)
    lookups = []

    # Define a list of fields we want to search by
    field_names = ['name', 'title', 'state', 'body']
    # Get our actual model query fields from our search models if they're in field_names
    for model in search_models:
        fields = [x for x in model._meta.get_fields() if x.name in field_names]

        # Start building queries
        search_queries = []
        for field in fields:
            # Set search text to pass to query based on active database type
            # For development Sqlite database
            if db_engine == 'django.db.backends.sqlite3':
                search_text = "__icontains"
            # For production Postgres database
            elif db_engine == 'django.db.backends.postgresql':
                search_text = "__search"

            # Build our queries from our search text, fields, and our search term from the frontend
            q_object = Q(**{field.name + search_text : form.cleaned_data['master_search']})
            search_queries.append(q_object)
        
        # Chain our field queries together before passing them to filer() below
        q_object = Q()
        for query in search_queries:
            # Check if our search term is in field1 OR field2 OR field3 etc.
            q_object = q_object | query
        
        # Query each model by our chained q_object and add to results
        results = model.objects.filter(q_object)
        lookups.append(results)

    # Sort our search results by model type and date created then return to our structured method below
    results_list = sorted(chain.from_iterable(lookups), key=lambda instance: instance.created_at)
    return results_list


# Given a form from our search view, call our get_search_results method above and split the results by model
def get_structured_search_results(form):
    results_list = get_search_results(form)

    # Define seperate lists for each model type
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
    # Return our lists to our view so we can add them to context
    return(issues, repos, folders, files)


#################################################################################################################################
# END
#################################################################################################################################
