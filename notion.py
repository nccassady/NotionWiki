from time import sleep
import notion_client

from getMushroomData import get_mushroom_data

client = notion_client.Client(auth="")
databaseId = ""

my_page = client.databases.query(
    **{
        "database_id": databaseId,
    }
)

wikiLabelIDsToNotionProperties = {
    # "(P18)": "image",
    # "(P225)": "Scientific Name",
    "(P783)": "Hymenium Type",
    "(P784)": "Cap Shape",
    "(P785)": "Hymenium Attachment",
    "(P787)": "Spore Color",
    "(P788)": "Ecological Role",
    "(P789)": "Edibility",
    "(P1843)": "Other Names",
}


def update(pages):
    for page in pages["results"]:
        if page["properties"]["Scientific Name"]["title"]:
            name = page["properties"]["Scientific Name"]["title"][0]["plain_text"]
            data = get_mushroom_data(name)

            if data:
                if "aliases" in data:
                    client.pages.update(
                        page_id=page["id"],
                        properties={
                            "Aliases": {
                                "rich_text": [{"text": {"content": ", ".join(data["aliases"])}}]
                            }
                        },
                    )

                for wikiKey, value in data["wikidata"].items():
                    for id, property in wikiLabelIDsToNotionProperties.items():
                        if id in wikiKey and property in page["properties"]:
                            if type(value) == str:
                                # Get info without id
                                newValue = value.split(" (")[0]

                                # Push to notion
                                try:
                                    client.pages.update(
                                        page_id=page["id"],
                                        properties={
                                            property: {
                                                "rich_text": [
                                                    {"text": {"content": newValue}}
                                                ]
                                            }
                                        },
                                    )
                                except Exception as e:
                                    print(
                                        f"Could not update {property} for {name} because:\n{e}"
                                    )
            else:
                print(f"Could not find data for {name}")


def update_all():
    my_page = client.databases.query(
        **{
            "database_id": databaseId,
        }
    )

    update(my_page)


def update_by_name(name):
    my_page = client.databases.query(
        **{
            "database_id": databaseId,
            "filter": {
                "property": "Name",
                "text": {
                    "contains": name,
                },
            },
        }
    )

    update(my_page)


# update_by_name("Cloud ear fungus")
update_all()
