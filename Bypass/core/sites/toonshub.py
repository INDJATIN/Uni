import requests
from re import search, match
from bs4 import BeautifulSoup
from urllib.parse import urlparse

async def toonshub_main(url):
    if search(r'.*/episode/.*', url):
        return await toons_episode(url)
    elif search(r'.*redirect.*', url):
        return
    else:
        return await toonshub_scraper(url)
      
async def toonshub_scraper(url):
    msg = ""
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    sub = soup.find_all('a',{'class':'shortc-button medium button'})
    for s in sub:
        item = s['href'].split('/')
        msg += f"<b>{item[4]} {item[3]} {item[-1]}</b>\n {s['href']}\n\n"
    return msg
    
def toons_episode(url):
    raw = urlparse(url)
    main = f"{raw.scheme}://{raw.netloc}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    item = soup.find_all('a', {'target': '_blank'})
    result = ""
    result += f"<b><u>{soup.find('title').get_text(strip=True)}</u></b>\n\n"
    resolution = []
    quality = soup.find_all('h5')
    for q in quality:
        if match(r'.*(480|1080|720|2160).*', q.text):
            resolution.append(q.text)
    filepress = []
    pixeldrain = []
    mirror = []
    for i in item:
        if "FileBee" in i.text:
            msg = f"<a href={main}{i['href']}>FileBee</a>"
            filepress.append(msg)
        elif "Pixeldrain" in i.text:
            msg = f"<a href={main}{i['href']}>Pixeldrain</a>"
            pixeldrain.append(msg)
        elif "Mirror" in i.text:
            msg = f"<a href={main}{i['href']}>Mirror</a>"
            mirror.append(msg)
    for r, f, p, m in zip(resolution, filepress, pixeldrain, mirror):
        result += f"<b>Quality : {r}</b>\n{f}    {p}   {m}\n"
    return result
