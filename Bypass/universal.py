from Bypass.core.sites.toonshub import toonshub_main

async def universal(url, message):
     reply = await sendMessage(message, "Bypassing....")
     result = ""
     if "toonshub" in url:
         result += await toonshub_main(url)
     else:
         return
     await editMessage(reply, result)
