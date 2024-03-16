from Bypass.core.sites.toonshub import toonshub_main
from Bypass.helper.message_utils import editMessage, sendMessage, deleteMessage

async def universal(url, message):
     reply = await sendMessage(message, "Bypassing....")
     result = ""
     if "toonshub" in url:
         result += await toonshub_main(url)
     else:
         return
     await editMessage(reply, result)
