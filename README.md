# aws-news-generator

Use ChatGPT to take an RSS feed and summary the news items into an easy to read article. This is very much a work in progress, mostly it doesn't work yet.

## How it works

* Pull last 7 days of news items from AWS RSS feed (done)
* Extract the needed info from the RSS feed items(done)
* Develop a good ChatGPT prompt to pass in the RSS feed items and create a useful article from the news items (In progress)
* Ask ChatGPT to write a catchy title (manual)
* Utilize an AI image generator to make a thumbnail (Manual)
* Run this lambda weekly to and store news to DynamoDB
* Create a simple and lightweight webpage to display the article
* Automate posting to Hacker News and Reddit
* Create my an RSS feed for these weekly summarized article
* Document how this can be used for other RSS feeds and create an easy to follow guide
