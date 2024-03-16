from pyrogram import Client, filters
from bs4 import BeautifulSoup
import requests

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot = Client("my_bot", bot_token='7059380834:AAGHzI3KZc8RjEqoT6JjbTYsMmmy5zh9nC4')

@bot.on_message(filters.command('start'))
def start_command(client, message):
    message.reply_text("Send me a link to scrape data!")

@bot.on_message(filters.regex(r'https?://\S+'))
def scrape_data(client, message):
    url = message.text
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    # Scrape the data
    for item in soup.find_all('your_tag_here'):
        title = item.find('your_title_tag_here').text
        link = item.find('your_link_tag_here')['href']
        size = item.find('your_size_tag_here').text
        data.append({'title': title, 'link': link, 'size': size})

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
