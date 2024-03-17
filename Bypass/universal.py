from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Bypass.core.sites.toonshub import toonshub_main
from Bypass.core.sites.kayoanime import kayoanime
from Bypass.helper.message_utils import editMessage, sendMessage, deleteMessage


async def universal(url, message):
    reply = await sendMessage(message, "Bypassing....")
    result = ""
    if "toonshub" in url:
        result += await toonshub_main(url)
    elif "kayoanime" in url:
        result += await kayoanime(url)
    else:
        return "No Bypass Found"
    await reply.edit_text(result,
                          reply_markup=InlineKeyboardMarkup([
                               [InlineKeyboardButton('🎓 Support Group', url='https://t.me/uni_bypasser')]
                          ])
                         )

