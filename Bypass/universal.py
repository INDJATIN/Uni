from bot.core.sites.toonshub import toonshub_main

async def universal(url):
     if "toonshub" in url:
         return await toonshub_main(url)
     else:
         return
