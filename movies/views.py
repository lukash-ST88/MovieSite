from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, DetailView
from .forms import ReviewsForm, RatingForm
from .models import *
from django.conf import settings


class GenreYear():
    def get_genre(self):
        return Genre.objects.all()

    def get_year(self):
        return Movie.objects.filter(draft=False)


class MoviesView(GenreYear, ListView):
    """список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    template_name = 'movies/movies.html'
    context_object_name = 'list_of_movies'
    paginate_by = 2

    # def get_context_data(self, *args, object_list=None, **kwargs):
    #     context = super().get_context_data(*args, **kwargs)
    #     context['category'] = Category.objects.all
    #     return context


class CategoryMovieView(GenreYear, ListView):
    model = Movie
    template_name = 'movies/movies.html'
    context_object_name = 'list_of_movies'
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(cat__url=self.kwargs['cat_url'])



class MovieDetailView(GenreYear, DetailView):
    """Данные фильма"""
    model = Movie
    template_name = 'movies/movie_detail.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug_movie'  # kwarg для файла url
    slug_field = 'url'  # по какому полю модели использовать url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context['form'] = ReviewsForm()
        return context


class AddReview(View):
    """создание отзывов"""

    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        # movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)  # для задержки сохранения
            if request.POST.get('parent', None):  # если parent отсутствует вернет none и if = false
                form.parent_id = int(request.POST.get('parent'))  # возвращается строка так как форма в html строчная
                print(request.POST)  # просто посмотреть что передается
            # form.movie = movie
            form.movie_id = pk
            form.save()

        return redirect('movie_detail',
                        slug_movie=Movie.objects.get(id=pk).url)  # раньше работало slug_movie=form.movie.url


class DirectorActor(GenreYear, DetailView):
    """блок описания режиссера и актера"""
    model = DirectorActor
    template_name = 'movies/DirectorActor.html'
    slug_field = 'name'
    context_object_name = 'Diract'


class FilterMovie(GenreYear, ListView):
    template_name = 'movies/movies.html'
    context_object_name = 'list_of_movies'
    paginate_by = 2

    def get_queryset(self):
        print(self.request.GET)
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist("year")) |
                                        Q(genre__in=self.request.GET.getlist("genre"))).distinct()
        print(self.request.GET.getlist('genre'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
        return context


"""ВОЗМОЖНАЯ РЕАЛИЗАЦИЯ ЧЕРЕЗ AJAX"""


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genre__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """определяем id клиента"""

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(ip=self.get_client_ip(request), movie_id=int(request.POST.get('movie')),
                                            defaults={'stars_id': int(request.POST.get('star'))})
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class SearchView(GenreYear, ListView):
    template_name = 'movies/movies.html'
    context_object_name = 'list_of_movies'
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))

    def get_context_data(self, *args, **kwargs):  # для работы пагинации на всех страницах
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f"q={self.request.GET.get('q')}&"
        return context
