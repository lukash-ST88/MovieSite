from modeltranslation.translator import register, TranslationOptions
from .models import Category, DirectorActor, Movie, Genre, Frame


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(DirectorActor)
class DirectorActorTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


@register(Movie)
class MovieTranslationOptions(TranslationOptions):
    fields = ('title', 'tagline', 'description', 'country')


@register(Frame)
class FrameTranslationOptions(TranslationOptions):
    fields = ('title', 'description')
