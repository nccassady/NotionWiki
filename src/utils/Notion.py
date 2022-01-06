import logging
import re

import notion_client

log = logging.getLogger()


class Notion:
    def __init__(self, secretKey: str, databaseId: str):
        """Create Notion client

        Args:
            secretKey (str): Your Integration Token
            databaseId (str): ID of the database to update
        """
        self.client = notion_client.Client(auth=secretKey)
        self.databaseId = databaseId
        self.database = self.client.databases.retrieve(database_id=databaseId)
        self.properties = self.database["properties"]
        self.mapping = {}
        log.debug("Notion client created")

    def checkForUpdateColumn(self):
        """Checks if database has a checkbox property with 'update' in the name

        Returns:
            str: Name of the update columne
            False: If none is found
        """
        updateColumn = False

        for name, data in self.properties.items():
            if data["type"] == "checkbox" and "update" in name.lower():
                log.info("Update column found")
                updateColumn = name

        return updateColumn

    def getWikiDataIds(self):
        """Get a list of the keys used by the database

        Returns:
            list[str]: IDs used
        """
        return self.getIdColumnMapping().keys()

    def getIdColumnMapping(self):
        """Gets a mapping of Wikidata IDs to Notion Column Names
            (e.g. {"P225": "Scientific Name (P225)"})

        Returns:
            dict: [str, str]
        """

        if not self.mapping:
            log.info("Loading properties mapping")
            for name, properties in self.properties.items():
                pattern = re.compile(".*\((P\d*)\).*")
                matches = pattern.match(name)

                if matches:
                    self.mapping[matches.group(1)] = name

        return self.mapping

    def getPagesToUpdate(self):
        """Gets the pages to update. If there is an update column, it will filter to only pages where the Update box is checkd.

        Returns:
            list[page]: A list of the pages found
        """
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

    def updateTextProperty(self, pageId: str, propertyName: str, newValue: str):
        """Update a page's text property

        Args:
            pageId (str): Page to update
            propertyName (str): Name of the property
            newValue (str): String value to set

        Returns:
            str: Updated value
        """
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

    def updateImage(self, pageId: str, propertyName: str, newValue: str):
        """Update a page's image property

        Args:
            pageId (str): Page to update
            propertyName (str): Name of the property
            newValue (str): URL to the new image

        Returns:
            str: Updated value
        """
        self.client.pages.update(
            page_id=pageId,
            properties={
                propertyName: {
                    "files": [{"external": {"url": newValue}, "name": newValue}]
                },
                "Update?": {"checkbox": False},
            },
        )

        return newValue
