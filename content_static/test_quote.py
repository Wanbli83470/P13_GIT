import unittest
from .quote import *
import datetime

class TestFonctionGet(unittest.TestCase):

    def setUp(self):
        self.quote_test = QuoteWeek().get_quote_week()

    def test_get_quote(self):



if __name__ == '__main__':
    unittest.main()
