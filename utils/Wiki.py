import wptools


class Wiki:
    def __init__(self, search: str, labels: list[str] = None, silent: bool = True):
        """Load the wiki page from the Search string

        Args:
            search (str): Page name to load
            labels (list[str], optional): List of property IDs to filter search by (e.g. ["P225"]). Defaults to None.
            silent (bool, optional): Hide page loading output. Defaults to True.
        """
        self.page = wptools.page(search, silent)

        if labels:
            self.page.wanted_labels(labels=labels)

        try:
            self.page.get_wikidata()
        except:
            pass

    def getData(self):
        return self.page.data["wikidata"]
