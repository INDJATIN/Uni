from bot.core.sites.toonshub import toonshub_main

async def universal(url):
     if "toonshub" in url:
         return toonshub_main(url)
     else:
         return
