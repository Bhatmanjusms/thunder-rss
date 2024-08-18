import feedparser
import telegram
import time

# Telegram bot token
BOT_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
CHANNEL_ID = '@yourchannelname'  # Replace with your channel name or chat ID

# RSS feed URL
RSS_URL = 'https://skymovieshd.chat/rss-feed-url'

# Initialize the bot
bot = telegram.Bot(token=BOT_TOKEN)

def fetch_rss_feed():
    feed = feedparser.parse(RSS_URL)
    return feed.entries

def send_update(entry):
    message = f"**{entry.title}**\n{entry.link}"
    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode=telegram.ParseMode.MARKDOWN)

def main():
    sent_entries = set()
    
    while True:
        feed_entries = fetch_rss_feed()
        for entry in feed_entries:
            if entry.link not in sent_entries:
                send_update(entry)
                sent_entries.add(entry.link)
        
        time.sleep(300)  # Wait for 5 minutes before checking for new updates

if __name__ == '__main__':
    main()
