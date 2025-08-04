# core/utils.py
from django.utils.text import slugify

def unique_slugify(instance, value, slug_field_name='slug'):
    slug = slugify(value)
    model_class = instance.__class__
    counter = 1
    unique_slug = slug
    while model_class.objects.filter(**{slug_field_name: unique_slug}).exists():
        unique_slug = f'{slug}-{counter}'
        counter += 1
    return unique_slug
