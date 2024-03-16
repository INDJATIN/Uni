import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Bypass.core.sites.gdtot_bypasser import gdtot

bot = Client(
    "project",
    api_id=2381992,
    api_hash="661ce2469998288dbac1147e10ff4d44",
    bot_token="6815990321:AAHNRCp-LRze6LYrP0Goy4gP9EEQneIsNGo",
)

CHANNEL_ID = "gdtot_bypasser"


@bot.on_message(filters.command('start'))
async def start_command(client, message):
    await message.reply("Hey, I am Gdtot Bypasser Bot, Just Send Your Gdtot Links And Get Drive Links")


@bot.on_message(filters.regex(r'https?://\S+'))
async def scrape_data(client, message):
    if "gdtot" in message.text:
        if await user_joined_channel(client, message):
            reply = await message.reply("Bypassing")
            link = message.text
            result = await gdtot(link)
            await reply.edit(result)
    elif "gdtot" not in message.text:
        await message.reply("Sorry, Bot Supports Only Gdtot Links")


async def user_joined_channel(client, message):
    if not await client.get_chat_member(CHANNEL_ID, message.from_user.id):
        await message.reply(
            "Please join our channel to access this command.",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Join Channel", url=f"https://t.me/{CHANNEL_ID}")]]
            )
        )
        return False
    return True

bot.run()
