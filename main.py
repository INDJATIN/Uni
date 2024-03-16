from pyrogram import Client, filters
import pyrogram.tgcrypto

bot = Client(
    "project",
    api_id=2381992,
    api_hash="661ce2469998288dbac1147e10ff4d44",
    bot_token="7059380834:AAGHzI3KZc8RjEqoT6JjbTYsMmmy5zh9nC4",
)

@bot.on_message(filters.command('start'))
def start_command(client, message):
    message.reply_text("Send me a link to scrape data!")

bot.run()
