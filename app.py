import os
import re

from utils.Notion import Notion
from utils.Wiki import Wiki

notion = Notion(os.environ["api_secret"], os.environ["dataase_id"])

pages = notion.getPagesToUpdate()

wikiDataCodes = list(notion.getWikiDataIds())

dataColumnMappings = notion.getIdColumnMapping()

for page in pages:
    name = notion.getPageTitle(page)
    wiki = Wiki(name, labels=wikiDataCodes)

    data = wiki.getData()
    for label, value in data.items():
        id = re.compile(".*\((P\d*)\).*").match(label).group(1)

        if id in wikiDataCodes:
            propertyType = notion.getPropertyType(dataColumnMappings[id])
            if propertyType == "rich_text":
                notion.updateTextProperty(page["id"], dataColumnMappings[id], value)
