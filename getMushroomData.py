import wptools

# Q198851: choice mushroom


def get_mushroom_data(scientific_name: str):
    try:
        page = wptools.page(scientific_name, silent=True)
        page.get_wikidata(
            show=False,
        )
    except Exception as e:
        return None

    return page.data
