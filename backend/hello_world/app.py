import json
import feedparser
import logging
from bs4 import BeautifulSoup


def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def lambda_handler(event, context):
    # Setup logger
    logger = setup_logger()

    url = "https://aws.amazon.com/blogs/aws/feed/"
    feed = feedparser.parse(url)

    print("Feed Title:", feed.feed.title)
    print("Feed Link:", feed.feed.link)
    print("Feed Description:", feed.feed.description)
    print("\n")

    for entry in feed.entries:
        print("Title:", entry.title)
        print("Link:", entry.link)
        print("Published Date:", entry.published)
        print("Author:", entry.author)
        print("Summary:", entry.summary)
        print("Content:", html_to_text(entry.content[0].value)) #ToDo: Check if more than one content
        print("\n")

    # print(json.dumps(feed.entries))

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
