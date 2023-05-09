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

def get_feed_items(url, news_items, markdown_total_news_items):
    # Setup logger
    logger = setup_logger()

    feed = feedparser.parse(url)

    # print("Feed Title:", feed.feed.title)
    # print("Feed Link:", feed.feed.link)
    # print("Feed Description:", feed.feed.description)
    print("\n")

    for entry in feed.entries:
        if within_last_7_days(entry.published):
            entry_data = {}

            # print(entry)
            # print(entry.keys())

            # Extract data from item and save to news_items with other feed data
            entry_data['title'] = entry.title
            print("Title:", entry.title)

            # if 'title_detail' in entry:
            #     entry_data['title_detail'] = entry.title_detail
            #     print("title_detail:", entry.title_detail)

            entry_data['link'] = entry.link
            print("Link:", entry.link)

            # Make markdown title with link
            markdown_total_news_items += f"### [{entry.title}]({entry.link})"

            # entry_data['published'] = entry.published
            # print("Published Date:", entry.published)

            # if 'author' in entry:
            #     entry_data['author'] = entry.author
            #     # print("Author:", entry.author)

            # Just another time stamp 
            # if 'published_parsed' in entry:
            #     entry_data['published_parsed'] = entry.published_parsed
            #     print("published_parsed:", entry.published_parsed)

            # if 'tags' in entry:
            #     entry_data['tags'] = entry.tags[0]['term']
            #     print("tags:", entry_data['tags'])

            # entry_data['summary'] = html_to_text(entry.summary)
            # print("Summary:", entry_data['summary'])
            markdown_total_news_items += f"\n{html_to_text(entry.summary)}"
            

            # if 'content' in entry:
            #     entry_data['content'] = html_to_text(entry.content[0].value)
            #     # print("Content:", html_to_text(entry.content[0].value)) #ToDo: Check if more than one content
            print("\n")

            news_items.append(entry_data)
            markdown_total_news_items += """
"""
            print(markdown_total_news_items)

def lambda_handler(event, context):

    # Prep storage for news items across feeds
    news_items = []
    blog_feeds = ('https://aws.amazon.com/blogs/aws/feed/', 'https://aws.amazon.com/blogs/architecture/feed/', 'https://aws.amazon.com/blogs/aws-cost-management/feed/', 'https://aws.amazon.com/blogs/apn/feed/', 'https://aws.amazon.com/podcasts/aws-podcast/', 'https://aws.amazon.com/blogs/awsmarketplace/feed/', 'https://aws.amazon.com/blogs/big-data/feed/', 'https://aws.amazon.com/blogs/business-productivity/feed/', 'https://aws.amazon.com/blogs/compute/feed/', 'https://aws.amazon.com/blogs/contact-center/feed/', 'https://aws.amazon.com/blogs/containers/feed/', 'https://aws.amazon.com/blogs/database/feed/', 'https://aws.amazon.com/blogs/desktop-and-application-streaming/feed/', 'https://aws.amazon.com/blogs/developer/feed/', 'https://aws.amazon.com/blogs/devops/feed/', 'https://aws.amazon.com/blogs/enterprise-strategy/feed/', 'https://aws.amazon.com/blogs/mobile/feed/', 'https://aws.amazon.com/blogs/gametech/feed/', 'https://aws.amazon.com/blogs/hpc/feed/', 'https://aws.amazon.com/blogs/infrastructure-and-automation/feed/', 'https://aws.amazon.com/blogs/industries/feed/', 'https://aws.amazon.com/blogs/iot/feed/', 'https://aws.amazon.com/blogs/machine-learning/feed/', 'https://aws.amazon.com/blogs/mt/feed/', 'https://aws.amazon.com/blogs/media/feed/', 'https://aws.amazon.com/blogs/messaging-and-targeting/feed/', 'https://aws.amazon.com/blogs/networking-and-content-delivery/feed/', 'https://aws.amazon.com/blogs/opensource/feed/', 'https://aws.amazon.com/blogs/publicsector/feed/', 'https://aws.amazon.com/blogs/quantum-computing/feed/', 'https://aws.amazon.com/blogs/robotics/feed/', 'https://aws.amazon.com/blogs/awsforsap/feed/', 'https://aws.amazon.com/blogs/security/feed/', 'https://aws.amazon.com/blogs/startups/feed/', 'https://aws.amazon.com/blogs/storage/feed/', 'https://aws.amazon.com/blogs/training-and-certification/feed/', 'https://aws.amazon.com/blogs/modernizing-with-aws/feed/')
    news_feeds = ('https://aws.amazon.com/about-aws/whats-new/recent/feed/',)

    # Create empty string to hold markdown in for new s
    markdown_total_news_items = """
"""

    # Process items in feeds
    for feed in news_feeds:
        print(f"Processing: {feed}")
        get_feed_items(feed, news_items, markdown_total_news_items)

    # print(news_items)
    print()

    # Ask AI to make summary
    # WARNING: ChatGPT can't take input this long. Need to figure out what to do about this.
    # completion = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo", 
    #     messages = [
    #         {"role": "system", "content" : "You are the writer of a summary of AWS News every week, given all items in the AWS news feed. You write in markdown. Start with a few paragraph summary of the biggest updates then write out all the updates with markdown links. Include all region names when mentioned."},
    #         {"role": "user", "content" : f"{news_items}"}
    #     ]
    # )

    # print(completion)
    # print('---------------------')
    # ai_summary = completion['choices'][0]['message']['content']
    # print(ai_summary)

    # Output markdown news items
    print("Markdown news items:")
    print(markdown_total_news_items)

# Prompts put into Chat GPT4 UI
# I want you to act as a developer and DevOps engineer who uses agile. I will provide you with the AWS news for the week. You will write an article that provides insightful commentary on the news topics at hand. You should use your own experiences, thoughtfully explain why something is important, back up claims with facts, and discuss potential use cases for new releases. Specifically use examples from your own work experience to apply these new updates. Your article will be written in markdown. Here is the news for the week:
# : <I paste in the json output from my lambda function>
# For the article, write a title which summarizes the updates and will get users on sites like Reddit and hacker news to click on it. 




