from Bypass import bot, LOGGER, Config
from pyrogram import idle
from pyrogram.filters import command, user
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from os import path as ospath, execl
from asyncio import create_subprocess_exec
from sys import executable
from Bypass.core.sites.gdtot_bypasser import gdtot

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
        await message.reply("Sorry, Bot Supports Only Gdtot Links")

@bot.on_message(filters.command('restart') & filters.user(Config.OWNER_ID))
async def restart(client, message):
    restart_message = await message.reply('<i>Restarting...</i>')
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    execl(executable, executable, "-m", "Bypass")

async def restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await Bypass.edit_message_text(chat_id=chat_id, message_id=msg_id, text="<i>Restarted !</i>")
        except Exception as e:
            LOGGER.error(e)

bot.start()
LOGGER.info('Bot Started!')
bot.loop.run_until_complete(restart())
idle()
bot.stop()