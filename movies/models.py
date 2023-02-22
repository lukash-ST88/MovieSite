from django.db import models
from datetime import date

from django.urls import reverse


class Category(models.Model):
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={"cat_url": self.url})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"




class Movie(models.Model):
    title = models.CharField("Название", max_length=150)
    tagline = models.CharField("Слоган", default='', max_length=200)
    description = models.TextField("Описание")
    poster = models.ImageField("Постер", upload_to='movies/')
    country = models.CharField("Страна", max_length=30)
    director = models.ManyToManyField('DirectorActor', verbose_name='Режиссер', related_name='movie_directors')
    actors = models.ManyToManyField('DirectorActor', verbose_name='Актеры', related_name='movie_actors')
    genre = models.ManyToManyField('Genre', verbose_name='Жанры')
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Указывать сумму в долларах")
    box_office_world = models.CharField("Сборы в мире", default=0, help_text="Указывать сумму в долларах", max_length=40)
    box_office_usa = models.CharField("Сборы в США", default=0, help_text="Указывать сумму в долларах", max_length=40)
    cat = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)
    url = models.SlugField(unique=True, max_length=160)
    draft = models.BooleanField("Черновик", default=False)
    year = models.PositiveSmallIntegerField("Год", null=True)

    def __str__(self):
        return self.title

    def get_reviews(self): # только отзывы у которых нет родителей
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug_movie': self.url})


class Frame(models.Model):
    title = models.CharField('Заголовок', max_length=150)
    description = models.TextField()
    image = models.ImageField("Изображение", upload_to='frames/')
    movie = models.ForeignKey(
        Movie, verbose_name="фильм", on_delete=models.CASCADE
    )  # при удалении фильма все связаные кадры тоже удалятся

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Кадр"
        verbose_name_plural = "Кадры"


class DirectorActor(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.SmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание")
    image = models.ImageField("Изображение", upload_to="directors_actors/")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Режиссеры и Актеры"
        verbose_name_plural = "Режиссеры и Актеры"

    def get_absolute_url(self): #сделать нормально
        return reverse('DirAct', kwargs={'slug': self.name})

class StarsOfRating(models.Model):
    value = models.PositiveSmallIntegerField("Значение", default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = "Звезды рейтинга "
        verbose_name_plural = "Общий рейтинг"
        ordering = ['value']

class Rating(models.Model):
    ip = models.CharField("IP адресс", max_length=15)
    stars = models.ForeignKey(StarsOfRating, verbose_name='звезда', on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.stars} - {self.movie}'

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=150)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey('self', verbose_name='родитель', on_delete=models.SET_NULL, null=True)
    movie = models.ForeignKey(Movie, verbose_name='фильм', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.movie}'

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Genre(models.Model):
    name = models.CharField("Имя", max_length=150)
    description = models.TextField("Описание")
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

