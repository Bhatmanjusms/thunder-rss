import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# URL of the website to scrape
website_url = 'https://skymovieshd.chat/'

def scrape_website():
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Assuming the website has a structure where each movie is in a specific HTML tag
    # You need to adjust the below selectors according to the actual structure of the site
    updates = []
    for post in soup.select('div.item'):  # Replace 'div.item' with the correct selector
        title = post.select_one('h2.title a').text  # Replace with actual title selector
        link = post.select_one('h2.title a')['href']  # Replace with actual link selector
        description = post.select_one('p.description').text  # Replace with actual description selector
        
        updates.append({
            'title': title,
            'link': link,
            'description': description
        })

    return updates

### Step 3: Generate the RSS Feed
Create the RSS feed using the data you've scraped.

```python
def generate_rss(updates):
    fg = FeedGenerator()
    fg.title('SkymoviesHD Updates')
    fg.link(href=website_url)
    fg.description('Latest updates from SkymoviesHD')

    for update in updates:
        fe = fg.add_entry()
        fe.title(update['title'])
        fe.link(href=update['link'])
        fe.description(update['description'])

    return fg.rss_str(pretty=True)  # Returns the RSS feed as a string

### Step 4: Serve the RSS Feed
You can serve the RSS feed using a simple Flask server.

```python
from flask import Flask, Response

app = Flask(__name__)

@app.route('/rss')
def rss_feed():
    updates = scrape_website()
    rss = generate_rss(updates)
    return Response(rss, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

### Step 5: Deploy and Host the Service
1. **Deploy the Flask app** on a server or a platform like Heroku.
2. Once deployed, you can access the RSS feed at `http://yourdomain.com/rss`.

### Step 6: Use the RSS Feed in Your Telegram Bot
Now that you have an RSS feed, you can use the script from my previous message to pull updates from this RSS feed and post them to your Telegram channel.

### Notes:
- The HTML structure of SkymoviesHD might change, so you’ll need to adjust the selectors in the scraper.
- Be cautious of the website's terms of service when scraping content.
