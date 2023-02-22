from django.test import SimpleTestCase
from movies.forms import *


class TestMovieForm(SimpleTestCase):
    def test_review_form_valid_date(self):
        form = ReviewsForm(data={
            'name': 'name1',
            'email': 'email1',
            'text': 'text1@txt.tx'
        })
        self.assertTrue(form.is_valid())

    def test_review_form_no_data(self):
        form = ReviewsForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 4)