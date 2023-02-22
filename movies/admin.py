from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms
from .models import *
from modeltranslation.admin import TranslationAdmin


from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    """Форма с виджетом ckeditor"""
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget()) #встроеные блоки редактирования на разных языках
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'



@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


class ReviewInline(
    admin.TabularInline):  # TabuluarInline выставляет поля по горизонтали, StackedInline собирает их в кучу
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1  # одно доп. пустое поле
    readonly_fields = ("name", "email")  # неизменяемые поля


class FramesInline(admin.StackedInline):
    model = Frame
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' height=auto width=50>")

    get_image.short_description = 'Изображение'


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Фильмы"""
    list_display = ("title", "cat", "url", "draft")
    list_filter = ("cat",)
    search_fields = ("title", "category__name")  # поля для поиска
    inlines = [ReviewInline, FramesInline]  # для добавления редактирования отзывов к фильму в редакторе фильмов
    actions = ['unpublish', 'publish'] # действия с гропой объектов
    form = MovieAdminForm
    save_on_top = True  # кнопка сохранения вверху
    save_as = True  # кнопка(сохранить дейтсвующие настройки как новый объект и продолжить редактирование)
    list_editable = ("draft",)  # возможность менять значение в общем списке объектов
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", "poster")
        }),
        (None, {
            "fields": (("year", "country"),)
        }),
        ("Directors and Actors", {
            "classes": ("collapse",),  # collapse - сслыка на вкладку с полями записи
            "fields": (("actors", "director", "genre", "cat"),)
        }),
        (None, {
            "fields": (("budget", "box_office_world", "box_office_usa"),)
        }),
        ("Options", {
            "fields": (("url", "draft"),)
        }),
    )  # для группировки полей по строкам. None, Options... - название группы(пишется в шапке строки)

    def unpublish(self, request, queryset):
        """снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            massege = "1 запись обновлена"
        else:
            massege = f'{row_update} записей обновлено'
        self.message_user(request, f'{massege}')

    def publish(self, request, queryset):
        """опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            massege = "1 запись обновлена"
        else:
            massege = f'{row_update} записей обновлено'
        self.message_user(request, f'{massege}')

    publish.allowed_permissions = ('change',)
    publish.short_description = "Опубликовать"

    unpublish.allowed_permissions = ('change',)
    unpublish.short_description = "Снять с публикации"



@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")  # не редактируемые поля при изменении экземпляра


@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    """Жанры"""
    list_display = ("name", "url")


class DirectorActorAdmin(TranslationAdmin):
    """Актеры"""
    list_display = ("name", "age", "get_image")

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' height=auto width=50>")

    get_image.short_description = 'Изображение'


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("ip",)


class FramesAdmin(TranslationAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_image")

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src='{obj.image.url}' height=auto width=50>")

    get_image.short_description = 'Изображение'


admin.site.register(DirectorActor, DirectorActorAdmin)
admin.site.register(StarsOfRating)
admin.site.register(Frame, FramesAdmin)
admin.site.site_title = 'Кино 88'
admin.site.site_header = 'Кино 88'

# to do
#TODO: настроить звезды

