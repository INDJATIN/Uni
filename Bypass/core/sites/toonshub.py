import requests
from re import search
from bs4 import BeautifulSoup

async def toonshub_main(url):
    if search(r'.*episode.*', url):
        return
    elif search(r'.*redirect.*', url):
        return
    else:
        return await toonshub_scraper(url)
      
async def toonshub_scraper(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    sub = soup.find_all('a',{'class':'shortc-button medium button'})
    for s in sub:
        item = s['href'].split('/')
        msg += f"<b>{item[4]} {item[3]} {item[-1]}</b>\n {s['href']}\n\n"
    return msg
