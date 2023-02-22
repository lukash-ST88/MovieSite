from django import template
from movies.models import *

register = template.Library()
# теги обычно используют в качестве замены миксинам

@register.simple_tag()
def category_tag():
    return Category.objects.all()


@register.inclusion_tag('tags/last_movies.html')
def last_movie_tag():
    movies = Movie.objects.order_by('id')[:2]
    return {'last_movies': movies}
