import requests
from re import search, compile
from bs4 import BeautifulSoup
from urllib.parse import urlparse

def turnstile(url):
    body = {
        "sitekey": "0x4AAAAAAADch0Ba3E6N-jTt",
        "url": url,
        "invisible": False
    }
    r = requests.post("https://dirty-agneta-studentworks3.koyeb.app/solve", json=body)
    token = r.json()['token']
    return token

def gdtot_cfl(url, session):
    res = session.get(url)
    raw = urlparse(url)
    secret_key = search(r'secret_key: "(.*?)"', str(res.text)).group(1)
    get_id = search(r'get_id : "(.*?)"', str(res.text)).group(1)
    SessionID = search(r"SessionID : '(.*?)'", str(res.text)).group(1)
    data = {
       'SessionID': SessionID,
       'get_id': get_id,
       'secret_key': secret_key,
       'token': await turnstile(url)
    }

    headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': url,
    }
    resp = session.post(f"{raw.scheme}://{raw.netloc}/cfl", data=data, headers=headers, cookies=res.cookies)
    return resp.text

def gdtot(url):
    cookie = {'crypt': config_dict['GDTOT_CRYPT']}
    with requests.Session() as session:
        session.cookies.update(cookie)
        res = session.get(url)
        soup = BeautifulSoup(await gdtot_cfl(url, session), 'html.parser')
        dwnld = soup.find('input', {'name':'dwnld'})['value']
        fve = soup.find('input', {'name':'fve'})['value']
        u = await gdtot_click(url, dwnld, fve, session)
        return u

def gdtot_click(url, dwnld, fve, session):
    response = session.get(url)
    raw = urlparse(url)
    api = f"{raw.scheme}://{raw.netloc}/dld"
    data = {
        'dwnld': dwnld,
        'fve': fve,
    }
    headers = {
        'Referer': url,
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    res = session.post(api, headers=headers, data=data)
    pattern = r'URL=(https?://\S+)'
    match = search(pattern, res.text).group(1)
    resp = session.get(match).text
    soup = BeautifulSoup(resp,'html.parser')
    sub_link = soup.find_all('a', href=compile(r'.*drive.*open.*'))
    if sub_link:
        if sub_link is not None:
            for r in sub_link:
                return r['href']
    else:
        return 'File Not Found / User Rate Limited'
