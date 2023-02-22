from django.test import TestCase
from movies.models import *
from datetime import date


class TestMovieModel(TestCase):
    def setUp(self):
        self.doc = Category.objects.create(name="Док", description='доки', url='doc')
        self.tar = DirectorActor.objects.create(name="Тарантино", age=34, description='постмодернист')
        self.five = StarsOfRating.objects.create(value=5)
        self.TC = Genre.objects.create(name='Трагикомедия')
        self.bl = Movie.objects.create(title='Барри Линдон', tagline='Жизнь Барри', year=date(1975, 3, 1),
                                       description='У Барри было множество преключений', country='США',
                                       url='barrylyndon')
        self.bl.director.add(self.tar)

    def test_category_str(self):
        self.assertEqual(str(self.doc), 'Док')

    def test_director_actor_str(self):
        self.assertEqual(str(self.tar), 'Тарантино')

    def test_stars_of_rating_str(self):
        self.assertEqual(str(self.five), '5')

    def test_genre_str(self):
        self.assertEqual(str(self.TC), 'Трагикомедия')

    def test_movie_str(self):
        self.assertEqual(str(self.bl), 'Барри Линдон')

    def test_movie_get_absolute_url(self):
        self.assertEqual(self.bl.get_absolute_url(), '/ru/barrylyndon/')

    def test_movie_director(self):
        self.assertEqual(self.bl.director.count(), 1)


