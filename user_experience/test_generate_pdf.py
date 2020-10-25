import unittest
from generate_pdf import *
from pathlib import Path


class TestExportPdf(unittest.TestCase):

    def setUp(self):
        """Launch of the QuoteWeek module to obtain the result of its method"""
        ExportPdf.generate_pdf(email="ocuser@gmail.com", username="test")

    def test_pdf_is_exist(self):
        name_pdf = "formulaire_adhésion_test.pdf"
        my_directory_test = f"/home/thomas/Bureau/P13_ESTIVAL_THOMAS/user_experience/static/user_experience/{name_pdf}"
        p = Path(my_directory_test)
        self.assertEqual(p.is_file(), True)


if __name__ == '__main__':
    unittest.main()
