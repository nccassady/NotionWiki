import os

import notion_client

from ..src.utils.Notion import Notion

apiSecret = os.environ["api_secret"]
dbId = os.environ["database_id"]


class TestNotion:
    client = Notion(apiSecret, dbId)

    def test_new_instance(self):
        assert isinstance(self.client.client, notion_client.Client)
        assert "properties" in self.client.database
        assert len(self.client.properties) > 0

    def test_update_column_check(self):
        assert self.client.checkForUpdateColumn()

    def test_get_wikidata_ids(self):
        assert len(self.client.getWikiDataIds()) > 0
