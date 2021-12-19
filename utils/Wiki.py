import wptools


class Wiki:
    def __init__(self, search, labels=None, silent=True):
        self.page = wptools.page(search, silent)

        if labels:
            self.page.wanted_labels(labels=labels)

        try:
            self.page.get_wikidata()
        except:
            pass

    def getData(self):
        return self.page.data["wikidata"]
