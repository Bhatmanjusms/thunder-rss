import os
from flask import Flask, Response
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator

# Load environment variables
load_dotenv()

# Retrieve environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
SECRET_KEY = os.getenv('SECRET_KEY')
website_url = 'https://skymovieshd.chat/'  # Define the website URL

# Debugging output
print(f"TELEGRAM_BOT_TOKEN: {TELEGRAM_BOT_TOKEN}")

# Initialize Flask app
app = Flask(__name__)

# Initialize Telegram Bot and Application
bot = Bot(token=TELEGRAM_BOT_TOKEN)
application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Welcome! I am your SkymoviesHD RSS Bot. Use /latest to get the latest updates.')

async def latest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    updates = scrape_website()
    if updates:
        for update_info in updates:
            message = f"**{update_info['title']}**\n{update_info['link']}\n{update_info['description']}"
            await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='Markdown')
    else:
        await update.message.reply_text('No updates available at the moment.')

def scrape_website():
    response = requests.get(website_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    updates = []
    for post in soup.select('div.item'):  # Adjust selectors based on actual HTML structure
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
    fg.link(href=website_url)
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
    # Set up command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('latest', latest))

    # Start the Bot
    application.run_polling()

    # Start the Flask app
    port = int(os.getenv('PORT', 8080))  # Use the PORT environment variable or default to 5000
    app.run(host='0.0.0.0', port=port)
