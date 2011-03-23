from django.test import TestCase
from banner_rotator.models import Banner

class AdtoTest(TestCase):
    """
    Make sure management commands updates the database
    """
    fixtures = ['banner_rotator.json']

    def testBiasedChoice(self):
        """
        We can't test for randomness, however we can test
            for the function returning a single element
        """
        self.assertEqual(1, len([Banner.objects.biased_choice()]))
