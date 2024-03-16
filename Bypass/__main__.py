from Bypass import Bypass, LOGGER, Config
from pyrogram import idle
from pyrogram.filters import command, user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from os import path as ospath, execl
from asyncio import create_subprocess_exec
from sys import executable
from Bypass.core.sites.gdtot_bypasser import gdtot

@Bypass.on_message(filters.command('start'))
async def start_command(client, message):
    await message.reply("Hey, I am Gdtot Bypasser Bot, Just Send Your Gdtot Links And Get Drive Links")


@Bypass.on_message(filters.regex(r'https?://\S+'))
async def scrape_data(client, message):
    if "gdtot" in message.text:
        reply = await message.reply("Bypassing")
        link = message.text
        result = await gdtot(link)
        await reply.edit(result)
    elif "gdtot" not in message.text:
        await message.reply("Sorry, Bot Supports Only Gdtot Links")

bot.run()
