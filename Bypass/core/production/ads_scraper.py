import requests
from bs4 import BeautifulSoup
from time import sleep
from re import match
from urllib.parse import urlparse

async def cloudbypass(url):
    if match(r'.*(shrs|shareus).*', url):
        return await shareus(url)
    elif "evolinks" in url:
        return await evolinks(url)
    elif "gtlinks" in url:
        return await gtlinks(url)
    elif "shrinkme" in url:
        return await custom(url, "https://en.shrinke.me", "https://themezon.net", 15)
    elif "birdurls" in url:
        return await custom(url, "https://birdurls.com", "https://hit-films.com", 10)
    elif "owllink" in url:
        return await custom(url, "https://owllink.net", "https://hit-films.com", 10)
    elif "sheralinks" in url:
        return await custom(url, "https://sheralinks.com", "https://blogyindia.com", 1)
    elif match(r'.*earn2me.com.*', url):
        return await custom(url, "https://blog.filepresident.com", "https://easyworldbusiness.com", 5)
    elif "tnshort" in url:
        return await custom(url, "https://go.tnshort.net", "https://jrlinks.in", 4)
    elif "rocklinks" in url:
        return await custom(url, "https://lnks.primarchweb.in", "https://blog.disheye.com", 5)
    elif match(r'.*easysky.*', url):
        return await custom(url, "https://techy.veganab.co", "https://camdigest.com/", 2)
    elif "tii.la" in url:    
        return await tii_la(url)
    else:
        return "No Bypass Found"
    
async def custom(url, DOMAIN, ref, t):
    code = url.rstrip("/").split("/")[-1]
    res = requests.get(f"{DOMAIN}/{code}", headers={'Referer': ref})
    soup = BeautifulSoup(res.text, "html.parser")
    data = {inp.get('name'): inp.get('value') for inp in soup.find_all("input")}
    sleep(t)
    resp = requests.post(f"{DOMAIN}/links/go",data=data,headers={'X-Requested-With':'XMLHttpRequest'},cookies=res.cookies)
    return resp.json()['url']

async def tii_la(url):
    raw = urlparse(url)
    DOMAIN = f"{raw.scheme}://{raw.netloc}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    data = { inp.get('name'): inp.get('value') for inp in soup.find_all('input') }
    resp = requests.post(url, data=data, headers={'Referer' : 'https://blogtechh.com/'})
    soup_res = BeautifulSoup(resp.text,'html.parser')
    data_res = { inp.get('name'): inp.get('value') for inp in soup_res.find_all('input') }
    sleep(10)
    resp1 = requests.post(f"{DOMAIN}/links/go", data=data_res, headers={'X-Requested-With': 'XMLHttpRequest'}, cookies=resp.cookies)
    return resp1.json()['url']

async def shareus(url):
    code = url.split('/')[-1]
    DOMAIN = f"https://api.shrslink.xyz"
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Origin':'https://shareus.io',
    }
    api = f"{DOMAIN}/v?shortid={code}&initial=true&referrer="
    id = requests.get(api, headers=headers).json()['sid']
    if not id:
        return "ID Error"
    else:
        api_2 = f"{DOMAIN}/get_link?sid={id}"
        res = requests.get(api_2, headers=headers)
        if res:
            final = res.json()['link_info']['destination']
            return final
            
async def gtlinks(url):
    code = url.split('/')[-1]
    useragent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    DOMAIN = "https://golink.gyanitheme.com"
    res = requests.get(f"{DOMAIN}/{code}", headers={'Referer':'https://tech.hipsonyc.com/','User-Agent': useragent})
    resp = requests.get(f"{DOMAIN}/{code}", headers={'Referer':'https://hipsonyc.com/','User-Agent': useragent}, cookies=res.cookies)
    soup = BeautifulSoup(resp.text,'html.parser')
    data = { inp.get('name'): inp.get('value') for inp in soup.find_all('input')}
    sleep(5)
    links = requests.post(f"{DOMAIN}/links/go", data=data, headers={'X-Requested-With':'XMLHttpRequest','User-Agent': useragent, 'Referer': f"{DOMAIN}/{code}"}, cookies=res.cookies)
    return links.json()['url']

async def evolinks(url):
    def linker(url):
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text,'html.parser')
        data = { inp.get('name'): inp.get('value') for inp in soup.find_all('input')}
        sleep(2)
        links = requests.post("https://ads.evolinks.in/links/go", data=data, headers={'X-Requested-With':'XMLHttpRequest', 'Referer': url}, cookies=resp.cookies)
        return links.json()['url']
    if 'ads' in url:
        return linker(url)
    else:
        new_url = url.replace('evolinks.in','ads.evolinks.in')
        return linker(new_url)
