from ..src.utils.Wiki import Wiki


class TestWiki:
    result = Wiki("Hericium erinaceus")

    def test_new_instance(self):
        assert self.result.page

    def test_load_data(self):
        self.result.getData()
        assert "requests" in self.result.page.data
        assert "wikidata" in self.result.page.data["requests"]
