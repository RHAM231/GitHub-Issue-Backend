import itertools
from django.template.defaultfilters import slugify
from issues import models
from repositories import models


# Let's create unique slugs for each model object from the object name using itertools.
# We'll also define a method for updating slugs if the name changes.
def generate_slug(instance, model):
    # Check which model we're using
    if hasattr(instance, 'name'):
        value = instance.name
    else:
        value = instance.title

    slug_candidate = slug_original = slugify(value).title() + '_' + str(1)
    # Count until we find an empty 'slot' for our slug
    for i in itertools.count(1):
        if not model.objects.filter(slug=slug_candidate).exists():
            break
        slug_candidate = '{}_{}'.format(slugify(value).title(), str(i))
    # If we're creating the first object, set slug to default value above
    if i == 1:
        slug_new = slug_original
    # Otherwise, set it based on itertools.count()
    else:
        slug_new = slug_candidate
    # For larger sites we would want to define a max_length for slugs
    instance.slug = slug_new
    return instance.slug