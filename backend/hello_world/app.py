import feedparser
import logging
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os
import openai

key=open("apikey", "r").readline()
openai.api_key = key

#########################

tokens_used = 0


# Get OpenAI auth
# openai.organization = "YOUR_ORG_ID"
# openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()



def setup_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    return logger

def within_last_7_days(date_string):
    date_format = "%a, %d %b %Y %H:%M:%S %z"
    date_obj = datetime.strptime(date_string, date_format)
    now = datetime.now(datetime.strptime("+0000", "%z").tzinfo)  # Assuming UTC timezone
    days_ago_7 = now - timedelta(days=7)
    return days_ago_7 <= date_obj <= now

def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text()

def get_feed_items(url, news_items):
    # Setup logger
    logger = setup_logger()

    feed = feedparser.parse(url)

    # print("Feed Title:", feed.feed.title)
    # print("Feed Link:", feed.feed.link)
    # print("Feed Description:", feed.feed.description)
    print("\n")

    n = 0
    for entry in feed.entries:
        if within_last_7_days(entry.published):
            news_items[n] = {}

            # print(entry)
            # print(entry.keys())

            # Extract data from item and save to news_items with other feed data
            news_items[n]['title'] = entry.title
            print("Title:", entry.title)

            # if 'title_detail' in entry:
            #     news_items[n]['title_detail'] = entry.title_detail
            #     print("title_detail:", entry.title_detail)

            news_items[n]['link'] = entry.link
            print("Link:", entry.link)

            news_items[n]['published'] = entry.published
            print("Published Date:", entry.published)

            if 'author' in entry:
                news_items[n]['author'] = entry.author
                # print("Author:", entry.author)

            # Just another time stamp 
            # if 'published_parsed' in entry:
            #     news_items[n]['published_parsed'] = entry.published_parsed
            #     print("published_parsed:", entry.published_parsed)

            if 'tags' in entry:
                news_items[n]['tags'] = entry.tags[0]['term']
                print("tags:", news_items[n]['tags'])

            news_items[n]['summary'] = html_to_text(entry.summary)
            print("Summary:", news_items[n]['summary'])
            

            if 'content' in entry:
                news_items[n]['content'] = html_to_text(entry.content[0].value)
                # print("Content:", html_to_text(entry.content[0].value)) #ToDo: Check if more than one content
            print("\n")

            n += 1


def lambda_handler(event, context):

    # Prep storage for news items across feeds
    news_items = {}

    blog_feeds = ('https://aws.amazon.com/blogs/aws/feed/', 'https://aws.amazon.com/blogs/architecture/feed/', 'https://aws.amazon.com/blogs/aws-cost-management/feed/', 'https://aws.amazon.com/blogs/apn/feed/', 'https://aws.amazon.com/podcasts/aws-podcast/', 'https://aws.amazon.com/blogs/awsmarketplace/feed/', 'https://aws.amazon.com/blogs/big-data/feed/', 'https://aws.amazon.com/blogs/business-productivity/feed/', 'https://aws.amazon.com/blogs/compute/feed/', 'https://aws.amazon.com/blogs/contact-center/feed/', 'https://aws.amazon.com/blogs/containers/feed/', 'https://aws.amazon.com/blogs/database/feed/', 'https://aws.amazon.com/blogs/desktop-and-application-streaming/feed/', 'https://aws.amazon.com/blogs/developer/feed/', 'https://aws.amazon.com/blogs/devops/feed/', 'https://aws.amazon.com/blogs/enterprise-strategy/feed/', 'https://aws.amazon.com/blogs/mobile/feed/', 'https://aws.amazon.com/blogs/gametech/feed/', 'https://aws.amazon.com/blogs/hpc/feed/', 'https://aws.amazon.com/blogs/infrastructure-and-automation/feed/', 'https://aws.amazon.com/blogs/industries/feed/', 'https://aws.amazon.com/blogs/iot/feed/', 'https://aws.amazon.com/blogs/machine-learning/feed/', 'https://aws.amazon.com/blogs/mt/feed/', 'https://aws.amazon.com/blogs/media/feed/', 'https://aws.amazon.com/blogs/messaging-and-targeting/feed/', 'https://aws.amazon.com/blogs/networking-and-content-delivery/feed/', 'https://aws.amazon.com/blogs/opensource/feed/', 'https://aws.amazon.com/blogs/publicsector/feed/', 'https://aws.amazon.com/blogs/quantum-computing/feed/', 'https://aws.amazon.com/blogs/robotics/feed/', 'https://aws.amazon.com/blogs/awsforsap/feed/', 'https://aws.amazon.com/blogs/security/feed/', 'https://aws.amazon.com/blogs/startups/feed/', 'https://aws.amazon.com/blogs/storage/feed/', 'https://aws.amazon.com/blogs/training-and-certification/feed/', 'https://aws.amazon.com/blogs/modernizing-with-aws/feed/')
    news_feeds = ('https://aws.amazon.com/about-aws/whats-new/recent/feed/', 'https://aws.amazon.com/blogs/aws/feed/')

    # Process items in feeds
    for feed in news_feeds:
        print(f"Processing: {feed}")
        get_feed_items(feed, news_items)

    # Ask AI to make summary
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Convert this list of AWS news items from an RSS feed into a weekly update for AWS users:\n\n{news_items}",
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    print("Chat GPT Summary")
    print(response)
