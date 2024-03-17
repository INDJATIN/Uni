import requests
from bs4 import BeautifulSoup

async def cinevood(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    titles = soup.select('h6')
    links_by_title = {}
    
    # Extract the post title from the webpage's title
    post_title = soup.title.string.strip()
    
    for title in titles:
        title_text = title.text.strip()
        gdtot_links = title.find_next('a', href=lambda href: "gdtot" in href.lower())
        multiup_links = title.find_next('a', href=lambda href: "multiup" in href.lower())
        filepress_links = title.find_next('a', href=lambda href: "filepress" in href.lower())
        gdflix_links = title.find_next('a', href=lambda href: "gdflix" in href.lower())
        kolop_links = title.find_next('a', href=lambda href: "kolop" in href.lower())
        zipylink_links = title.find_next('a', href=lambda href: "zipylink" in href.lower())
        
        links = []
        if gdtot_links:
            links.append(f'<a href="{gdtot_links["href"]}" style="text-decoration:none;"><b>GDToT</b></a>')
        if multiup_links:
            links.append(f'<a href="{multiup_links["href"]}" style="text-decoration:none;"><b>MultiUp</b></a>')
        if filepress_links:
            links.append(f'<a href="{filepress_links["href"]}" style="text-decoration:none;"><b>FilePress</b></a>')
        if gdflix_links:
            links.append(f'<a href="{gdflix_links["href"]}" style="text-decoration:none;"><b>GDFlix</b></a>')
        if kolop_links:
            links.append(f'<a href="{kolop_links["href"]}" style="text-decoration:none;"><b>Kolop</b></a>')
        if zipylink_links:
            links.append(f'<a href="{zipylink_links["href"]}" style="text-decoration:none;"><b>ZipyLink</b></a>')
        
        if links:
            links_by_title[title_text] = links
    
    prsd = f"<b>🔖 Title:</b> {post_title}\n"
    for title, links in links_by_title.items():
        prsd += f"\n┏<b>Name:</b> <code>{title}</code>\n"
        prsd += "┗<b>Links:</b> " + " | ".join(links) + "\n"
      
    return prsd
