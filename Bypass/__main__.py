from pyrogram import idle, Client
from pyrogram.enums import ParseMode
from pyrogram.filters import command, user, regex
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from time import time
from dotenv import load_dotenv
from os import path as ospath, execl, getenv
from asyncio import create_subprocess_exec
from sys import executable
from logging import getLogger, FileHandler, StreamHandler, INFO, ERROR, basicConfig
from uvloop import install

from Bypass.core.sites.gdtot_bypasser import gdtot

install()
basicConfig(format="[%(asctime)s] [%(levelname)s] - %(message)s", #  [%(filename)s:%(lineno)d]
            datefmt="%d-%b-%y %I:%M:%S %p",
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)

getLogger("pyrogram").setLevel(ERROR)
LOGGER = getLogger(__name__)

load_dotenv('config.env', override=True)
BOT_START = time()

class Config:
    BOT_TOKEN = getenv('BOT_TOKEN', '')
    API_HASH = getenv('API_HASH', '')
    API_ID = getenv('API_ID', '')
    if BOT_TOKEN == '' or API_HASH == '' or API_ID == '':
        LOGGER.critical('ENV Missing. Exiting Now...')
        exit(1)
    OWNER_ID = getenv('OWNER_ID','')
    GDTOT_CRYPT = getenv('GDTOT_CRYPT', '')
    
bot = Client("Diffusion", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, plugins=dict(root="Bypass/plugins"), parse_mode=ParseMode.HTML)

@bot.on_message(command('start'))
async def start_command(client, message):
    await message.reply("Hey, I am Gdtot Bypasser Bot, Just Send Your Gdtot Links And Get Drive Links")


@bot.on_message(regex(r'https?://\S+'))
async def scrape_data(client, message):
    if "gdtot" in message.text:
        reply = await message.reply("Bypassing")
        link = message.text
        result = await gdtot(link)
        await reply.edit(result)
    elif "gdtot" not in message.text:
        await message.reply("Sorry, Bot Supports Only Gdtot Links")

@bot.on_message(command('restart') & user(Config.OWNER_ID))
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
