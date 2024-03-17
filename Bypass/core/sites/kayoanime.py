import requests
import re
from bs4 import BeautifulSoup

async def kayoanime(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    msg = ""
    title = soup.find('h1').text
    msg += f"<b><i>Title : {title}</b></i>\n\n"
    pattern = re.compile(r'(Type|Episodes|Aired|Premiered|Status|Genres|Broadcast|Producers|Licensors|Source|Themes|Demographic|Duration|Rating): (.+)')
    matching_items = soup.find_all('li', string=pattern)
    for item in matching_items:
        msg += f"<b><i>{item.get_text()}</b></i>\n"
    msg += f"\n<b><i>Download Links : </b></i>\n\n"
    sub_links = soup.find_all('a', href=re.compile(r'.*tiny|drive|groups.*'))
    for sub_link in sub_links:
        dl_link = sub_link['href']
        dl_text = sub_link.text
        msg += f"<b><i>{dl_text}</b></i> : <a href={dl_link}>Click Here</a>\n"
    return msg
