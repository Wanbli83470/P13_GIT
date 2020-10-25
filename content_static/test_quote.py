import unittest
from quote import quotes, QuoteWeek
from freezegun import freeze_time


@freeze_time("2020-01-29")
class TestFonctionGet(unittest.TestCase):

    def setUp(self):
        self.quote_test = QuoteWeek().get_quote_week()
        print(self.quote_test)

    def test_get_quote(self):
        self.assertEqual(self.quote_test, quotes[5])


if __name__ == '__main__':
    unittest.main()
