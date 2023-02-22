from django.urls import path
from .views import *


urlpatterns = [
    path('', MoviesView.as_view(), name='home'),
    path('filter/', FilterMovie.as_view(), name='filter'),
    path('category/<slug:cat_url>', CategoryMovieView.as_view(), name='category'),
    path('search/', SearchView.as_view(), name='search'),
    path("add-rating/", AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", JsonFilterMoviesView.as_view(), name='json_filter'),
    path('<slug:slug_movie>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>', AddReview.as_view(), name='add_review'),
    path('DirectorActor/<str:slug>', DirectorActor.as_view(), name='DirAct')
]

