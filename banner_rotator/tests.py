from django.test import TestCase
from .managers import pick


class BaseBannerTest(TestCase):
    fixtures = ['test_data']


class BannerManagerTest(BaseBannerTest):

    def test_pick(self):
        # check with a item of probability 1
        choices = [
            (True, 1),
            (False, 0),
            (False, 0),
            (False, 0),
            (False, 0),
        ]
        result = pick(choices)
        self.assertTrue(result)

        # Ensure nothing funky happens if we have an
        # invalid probability distribution
        choices = [
            (True, 1),
            (True, 1),
            (False, 0),
            (False, 0),
            (False, 0),
        ]
        result = pick(choices)
        self.assertTrue(result)
