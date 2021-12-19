import re

import notion_client


class Notion:
    def __init__(self, secretKey, databaseId):
        self.client = notion_client.Client(auth=secretKey)
        self.databaseId = databaseId
        self.database = self.client.databases.retrieve(database_id=databaseId)
        self.properties = self.database["properties"]

    def checkForUpdateColumn(self):
        updateColumn = False

        for name, data in self.properties.items():
            if data["type"] == "checkbox" and "update" in name.lower():
                updateColumn = name

        return updateColumn

    def getWikiDataIds(self):
        return self.getIdColumnMapping().keys()

    def getIdColumnMapping(self):
        mapping = {}

        for name, properties in self.properties.items():
            pattern = re.compile(".*\((P\d*)\).*")
            matches = pattern.match(name)

            if matches:
                mapping[matches.group(1)] = name

        return mapping

    def getPagesToUpdate(self):
        updateColumn = self.checkForUpdateColumn()

        if updateColumn:
            updatePages = self.client.databases.query(
                **{
                    "database_id": self.databaseId,
                    "filter": {
                        "property": updateColumn,
                        "checkbox": {
                            "equals": True,
                        },
                    },
                }
            )
        else:
            updatePages = self.client.databases.query(
                **{
                    "database_id": self.databaseId,
                }
            )

        return updatePages["results"]

    def getPageTitle(self, page):
        return page["properties"]["Search"]["title"][0]["plain_text"]

    def getPropertyType(self, propertyName):
        return self.properties[propertyName]["type"]

    def updateProperty(self, pageId, propertyName, newValue):
        if type(newValue) == list:
            splitValues = [item.split(" (")[0] for item in newValue]
            newValue = ", ".join(splitValues)
        elif type(newValue) == str:
            newValue = newValue.split(" (")[0]

        self.client.pages.update(
            page_id=pageId,
            properties={
                propertyName: {"rich_text": [{"text": {"content": newValue}}]},
                "Update?": {"checkbox": False},
            },
        )

        return newValue
