from flask import Flask, Response
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# Load environment variables
load_dotenv()

# Flask application setup
app = Flask(__name__)

# Get environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')  # Provide a default if not set

# Define the URL of the website to scrape
website_url = 'https://skymovieshd.chat/'

def scrape_website():
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, 'html.parser')

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

    return fg.rss_str(pretty=True)

@app.route('/rss')
def rss_feed():
    updates = scrape_website()
    rss = generate_rss(updates)
    return Response(rss, mimetype='application/rss+xml')

if __name__ == '__main__':
    # Optional: Print out environment variables to ensure they're loaded correctly (for debugging purposes)
    print(f"Telegram Bot Token: {TELEGRAM_BOT_TOKEN}")
    print(f"Secret Key: {SECRET_KEY}")

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)
