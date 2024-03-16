import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from re import compile, search, match
from pyrogram import Client, filters
from gdtot_bypasser import gdtot

bot = Client(
    "project",
    api_id=2381992,
    api_hash="661ce2469998288dbac1147e10ff4d44",
    bot_token="6531755753:AAHGBmBD6-eiHZgPvmZjeGxG1Ge4-HKYE2E",
)

@bot.on_message(filters.command('start'))
async def start_command(client, message):
    await message.reply("Hey, I am Gdtot Bypasser Bot, just Send your Gdtot Links and get drive links")

@bot.on_message(filters.regex(r'https?://\S+'))
async def scrape_data(client, message):
    if "gdtot" in message.text:
        reply = await message.reply("Bypassing In 20 Seconds")
        link = message.text
        result = await gdtot(link)
        await reply.reply(result)
    elif "gdtot" not in message.text:
        await message.reply("Sorry , Bot Support Only Gdtot Links")

bot.run()
