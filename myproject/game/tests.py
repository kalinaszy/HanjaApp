from django.test import TestCase

# Create your tests here.
from django.urls import reverse
import factory

from game.models import Score


class ViewTest(TestCase):
    def test_views(self):
        response = self.client.get(reverse('euro'))
        self.assertEqual(response.status_code, 200)

    def trivial_test(self):
        before = Score.objects.count()
        Score.objects.create()
        after = Score.objects.count()
        self.assertEqual(before + 1, after)

