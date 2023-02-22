from django.test import SimpleTestCase
from movies.models import *
from django.urls import reverse, resolve
from movies.views import *

"""тест корректности связей url и view"""
class TestMovieURLs(SimpleTestCase):
    def test_movie_detail_url(self):
        url = reverse("movie_detail", args=['some-slug'])
        print(url) # возвращяет url путь
        print(resolve(url)) # возвращвет разложенный url запрос
        self.assertEqual(resolve(url).func.view_class, MovieDetailView)

