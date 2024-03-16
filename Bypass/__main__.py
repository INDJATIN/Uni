from Bypass import bot, LOGGER, Config
from pyrogram import idle
from os import path as ospath, execl
from asyncio import create_subprocess_exec
from sys import executable

from pyrogram.handlers import MessageHandler, CallbackQueryHandler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from pyrogram.filters import command, user, regex
from .helper.bot_commands import BotCommands

async def start(client, message):
    await message.reply(f'''<b><i>Bypass Bot!</i></b>
    
    <i>A Powerful Elegant Multi Threaded Bot written in Python... which can Bypass Various Shortener Links, Scrape links, and More ... </i>
    
    <i><b>Bot Started  ago...</b></i>

    ''',quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('🎓 Dev', url='https://t.me/SilentDemonSD'), InlineKeyboardButton('🔍 Deploy Own', url="https://github.com/SilentDemonSD/FZBypassBot")]
            ])
    )

@bot.on_message(regex(r'https?://\S+'))
async def scrape_data(client, message):
    await message.reply("Sorry, Bot Is Under Maintenance")

@bot.on_message(command('restart'))
async def restart(client, message):
    restart_message = await message.reply('<i>Restarting...</i>')
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    execl(executable, executable, "-m", "Bypass")

async def restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="<i>Restarted !</i>")
        except Exception as e:
            LOGGER.error(e)
def main():
    bot.add_handler(MessageHandler(
        start, filters=command(BotCommands.StartCommand) & private))
    LOGGER.info(f"Bypass Bot Started!")
    signal(SIGINT, exit_clean_up)

bot.loop.run_until_complete(main())
bot.loop.run_forever()
