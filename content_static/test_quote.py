import unittest
from quote import quotes, QuoteWeek
from freezegun import freeze_time


@freeze_time("2020-01-29")  # Simulation of the 5th week of the year
class TestFonctionGet(unittest.TestCase):

    def setUp(self):
        """Launch of the QuoteWeek module to obtain the result of its method"""
        self.quote_test = QuoteWeek().get_quote_week()
        print(self.quote_test)

    def test_get_quote(self):
        """Comparison between the theoretical result and the practical result"""
        self.assertEqual(self.quote_test, quotes[5])


if __name__ == '__main__':
    unittest.main()
