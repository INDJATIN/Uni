import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from re import compile, search, match
from pyrogram import Client, filters
from gdtot_bypasser import gdtot
from logging import getLogger

bot = Client(
    "project",
    api_id=2381992,
    api_hash="661ce2469998288dbac1147e10ff4d44",
    bot_token="6715308533:AAEVkp7wqYv0fwTiJdZGrRAXt1ygMsxqg-s",
)
LOGGER = getLogger(__name__)

@bot.on_message(filters.command('start'))
async def start_command(client, message):
    await message.reply("Hey, I am Gdtot Bypasser Bot, Just Send Your Gdtot Links And Get Drive Links")

@bot.on_message(filters.regex(r'https?://\S+'))
async def scrape_data(client, message):
    if "gdtot" in message.text:
        reply = await message.reply("Bypassing")
        link = message.text
        result = await gdtot(link)
        await reply.edit(result)
    elif "gdtot" not in message.text:
        await message.reply("Sorry , Bot Support Only Gdtot Links")

LOGGER.info("Bot Started")
bot.run()
