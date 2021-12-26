import re

from utils.Notion import Notion
from utils.Wiki import Wiki


def run(notionClient):

    pages = notionClient.getPagesToUpdate()

    wikiDataCodes = list(notionClient.getWikiDataIds())

    dataColumnMappings = notionClient.getIdColumnMapping()
    itemsUpdated = 0
    for page in pages:
        name = notionClient.getPageTitle(page)
        wiki = Wiki(name, labels=wikiDataCodes)

        data = wiki.getData()
        for label, value in data.items():
            id = re.compile(".*\((P\d*)\).*").match(label).group(1)

            if id in wikiDataCodes:
                propertyType = notionClient.getPropertyType(dataColumnMappings[id])
                if propertyType == "rich_text":
                    notionClient.updateTextProperty(
                        page["id"], dataColumnMappings[id], value
                    )
                    itemsUpdated += 1

    return itemsUpdated


def lambda_handler(event, context):
    """
    Accepts an action and a number, performs the specified action on the number,
    and returns the result.
    :param event: The event dict that contains the parameters sent when the function
                    is invoked.
    :param context: The context in which the function is called.
    :return: The result of the specified action.
    """
    notion = Notion(event["api_secret"], event["database_id"])

    result = run(notion)
    response = {"result": result}
    return response
