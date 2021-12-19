import unittest

import config
import notion_client
from utils.Notion import Notion


class TestNotion(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.client = Notion(config.API_SECRET, config.DATABASE_ID)

    def test_new_instance(self):
        self.assertIsInstance(self.client.client, notion_client.Client)
        self.assertIn("properties", self.client.database)
        self.assertGreater(len(self.client.properties), 0)

    def test_update_column_check(self):
        self.assertNotEqual(False, self.client.checkForUpdateColumn())

    def test_get_wikidata_ids(self):
        self.assertGreater(len(self.client.getWikiDataIds()), 0)


if __name__ == "__main__":
    unittest.main()
