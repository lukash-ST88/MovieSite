from datetime import date

from django.test import TestCase, Client
from django.urls import reverse
from movies.models import *
import json

class TestMovieViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.detail_url = reverse('movie_detail', args=['barrylyndon'])
        self.add_review_url = reverse('add_review', args=[1])
        self.BL = Movie.objects.create(title='Барри Линдон', tagline='Жизнь Барри',
                             poster='C:\\Users\\Station-88\\PycharmProjects\\Python\\MovieSite\\MovieSite\\media\\directors_actors\\Quentin.jpg',
                             year=date(1975, 3, 1), description='У Барри было множество преключений', country='США',
                                       url='barrylyndon')

    def test_movie_list_GET(self): # тест по GET запросу списка фильмов
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movies.html')

    def test_movie_detail_GET(self): # тест по GET запросу списка фильмов
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies/movie_detail.html')

    def test_movie_detail_review_POST_no_data(self):
        self.assertEqual(self.BL.reviews_set.count(), 0)

    # def test_movie_detail_review_POST(self):
    #     response = self.client.post(self.add_review_url, {
    #         'text': 'text',
    #         'name': 'name1',
    #         'email': 'ema12@ads.ru'
    #     })
    #     self.assertEqual(self.BL.reviews_set.first().name, 'name1')
