import unittest

import wptools
from utils.Wiki import Wiki


class TestWiki(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.result = Wiki("Hericium erinaceus")

    def test_new_instance(self):
        self.assertIsInstance(self.result.page, wptools.page)

    def test_load_data(self):
        self.result.load_data()
        self.assertIn("requests", self.result.page.data)
        self.assertIn("wikidata", self.result.page.data["requests"])


if __name__ == "__main__":
    unittest.main()
