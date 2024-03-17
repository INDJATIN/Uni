import requests 
from bs4 import BeautifulSoup

async def skymovieshd(url):
    res = requests.get(url, allow_redirects=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    t = soup.select('div[class^="Robiul"]')
    gd_txt = f"<i>{t[-1].text.replace('Download ', '')}</i>"
    _cache = []
    for link in soup.select('a[href*="howblogs.xyz"]'):
        if link['href'] in _cache:
            continue
        _cache.append(link['href'])
        gd_txt += f"\n\n<b>{link.text} :</b> \n"
        resp = requests.get(link['href'], allow_redirects=False)
        nsoup = BeautifulSoup(resp.text, 'html.parser') 
        atag = nsoup.select('div[class="cotent-box"] > a[href]')
        for no, link in enumerate(atag, start=1): 
            gd_txt += f"{no}. {link['href']}\n"
    return gd_txt
