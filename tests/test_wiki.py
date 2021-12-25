import wptools
from ..utils.Wiki import Wiki


class TestWiki:
    result = Wiki("Hericium erinaceus")

    def test_new_instance(self):
        assert isinstance(self.result.page, wptools.page)

    def test_load_data(self):
        self.result.getData()
        assert "requests" in self.result.page.data
        assert "wikidata" in self.result.page.data["requests"]
