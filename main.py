import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from re import compile, search, match
from pyrogram import Client, filters

bot = Client(
    "project",
    api_id=2381992,
    api_hash="661ce2469998288dbac1147e10ff4d44",
    bot_token="7059380834:AAGHzI3KZc8RjEqoT6JjbTYsMmmy5zh9nC4",
)

def res_soup(url, word):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    sub_links = soup.find_all('a', href=compile(fr'.*{word}.*'))
    valid_links = [link['href'] for link in sub_links if link.get('href')]
    return valid_links

def url_check(url):
    raw = urlparse(url)
    res = requests.get(url)
    m = search(r'replace.*"(.*)"', res.text)
    if m:
        id = m.group(1)
        u = f"{raw.scheme}://{raw.netloc}{id}"
        if "404" not in u:
            return u

@bot.on_message(filters.command('start'))
def start_command(client, message):
    message.reply_text("Send me a link to scrape data!")

@bot.on_message(filters.regex(r'https?://\S+'))
def scrape_data(client, message):
    args = message.text
    res = res_soup(args, "archives")
    data = []
    for link in res:
        resp = res_soup(link, "getlink")
        for cat in resp:
            mad = res_soup(cat, "key")
            for hn in mad:
                final = url_check(hn)
                res = requests.get(final)
                soup = BeautifulSoup(res.text, 'html.parser')
                items = soup.find_all('li', {'class': 'list-group-item'})
                title = ''
                size = ''
                for item in items:
                    text = item.text
                    if not match(r'.*(Format|Added).*', text):
                        if "Name" in text:
                            title = text
                        elif "Size" in text:
                            size = text
                        url = final
                        data.append({'title': title, 'link': url, 'size': size})

    # Split data into chunks of 5 items
    chunks = [data[i:i + 5] for i in range(0, len(data), 5)]
    current_page = 0
                
    def generate_markup():
        return {
            'inline_keyboard': [
                [{'text': 'Previous', 'callback_data': 'prev'}, {'text': 'Next', 'callback_data': 'next'}]
            ]
        }

    def edit_chunk(chat_id, message_id, page):
        items = chunks[page]
        text = '\n'.join([f"{i+1}. {item['title']} - {item['size']} - {item['link']}" for i, item in enumerate(items)])
        bot.edit_message_text(chat_id, message_id, text, reply_markup=generate_markup())

    @bot.on_callback_query()
    def on_callback_query(client, callback_query):
        nonlocal current_page
        chat_id = callback_query.message.chat.id
        message_id = callback_query.message.message_id
        if callback_query.data == 'prev':
            current_page = (current_page - 1) % len(chunks)
        elif callback_query.data == 'next':
            current_page = (current_page + 1) % len(chunks)
        edit_chunk(chat_id, message_id, current_page)
        bot.answer_callback_query(callback_query.id)

    edit_chunk(message.chat.id, message.message_id, current_page)
bot.run()
