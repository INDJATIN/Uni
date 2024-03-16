from os import getenv
from time import time
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.enums import ParseMode
from logging import getLogger, FileHandler, StreamHandler, INFO, ERROR, basicConfig
from uvloop import install

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
    FSUB_IDS = getenv('FSUB_IDS','')
    GDTOT_CRYPT = getenv('GDTOT_CRYPT', '')
    
bot = Client("Diffusion", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN, parse_mode=ParseMode.HTML)
