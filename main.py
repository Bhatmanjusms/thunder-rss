from flask import Flask, Response
from telegram import Bot
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# Load environment variables
load_dotenv()

# Configuration from environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')  # e.g., '@yourchannelname'
RSS_FEED_URL = os.getenv('RSS_FEED_URL')
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

def scrape_website():
    response = requests.get(RSS_FEED_URL)
    soup = BeautifulSoup(response.text, 'html.parser')

    updates = []
    for post in soup.select('div.item'):  # Adjust selectors according to the actual HTML structure
        title = post.select_one('h2.title a').text
        link = post.select_one('h2.title a')['href']
        description = post.select_one('p.description').text
        
        updates.append({
            'title': title,
            'link': link,
            'description': description
        })

    return updates

def generate_rss(updates):
    fg = FeedGenerator()
    fg.title('SkymoviesHD Updates')
    fg.link(href=RSS_FEED_URL)
    fg.description('Latest updates from SkymoviesHD')

    for update in updates:
        fe = fg.add_entry()
        fe.title(update['title'])
        fe.link(href=update['link'])
        fe.description(update['description'])

    return fg.rss_str(pretty=True)

def send_updates_to_telegram(updates):
    for update in updates:
        message = f"**{update['title']}**\n{update['link']}\n{update['description']}"
        bot.send_message(chat_id=TELEGRAM_CHANNEL_ID, text=message, parse_mode='Markdown')

@app.route('/rss')
def rss_feed():
    updates = scrape_website()
    send_updates_to_telegram(updates)
    rss = generate_rss(updates)
    return Response(rss, mimetype='application/rss+xml')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
