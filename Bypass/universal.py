from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Bypass.core.sites.cinevood import cinevood
from Bypass.core.sites.toonshub import toonshub_main
from Bypass.core.sites.kayoanime import kayoanime
from Bypass.core.production.ads_scraper import cloudbypass
from Bypass.helper.message_utils import editMessage, sendMessage, deleteMessage

async def universal(url, message):
    result = ""
    if "toonshub" in url:
        reply = await sendMessage(message, "Bypassing....")
        result += await toonshub_main(url)
    elif "kayoanime" in url:
        reply = await sendMessage(message, "Getting Contents and Details")
        result += await kayoanime(url)
    elif "cinevood" in url:
        reply = await sendMessage(message, "Getting Contents and Details")
        result += await cinevood(url)
    elif "" in url:
        reply = await sendMessage(message, "Bypassing Ads...")
        result += await cloudbypass(url)
    else:
        return "No Bypass Found"
    await reply.edit_text(result,
                          reply_markup=InlineKeyboardMarkup([
                               [InlineKeyboardButton('🎓 Support Group', url='https://t.me/uni_bypasser')]
                          ])
                         )                 
