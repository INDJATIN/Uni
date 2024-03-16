import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from re import compile, search, match
from pyrogram import Client, filters

bot = Client(
    "project",
    api_id=2381992,
    api_hash="661ce2469998288dbac1147e10ff4d44",
    bot_token="6531755753:AAHGBmBD6-eiHZgPvmZjeGxG1Ge4-HKYE2E",
)

@bot.on_message(filters.command('start'))
def start_command(client, message):
    message.reply_text("Hey, I am Gdtot Bypasser Bot, just Send your Gdtot Links and get drive links")

@bot.on_message(filters.regex(r'https?://\S+'))
def scrape_data(client, message):
    if "gdtot" in message.text:
        message.reply_text("Tested")
    elif "gdtot" not in message.text:
        message.reply_text("Sorry , Bot Support Only Gdtot Link")

bot.run()
