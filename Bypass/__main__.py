from Bypass import bot, LOGGER, Config
from pyrogram import idle
from os import path as ospath, execl
from asyncio import create_subprocess_exec
from sys import executable
from signal import signal, SIGINT

from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.filters import command, private, regex
from .helper.bot_commands import BotCommands

async def start(client, message):
    await message.reply_text(
        f'''<b> Universal Bot With Light Weight Functions To Get Your Destination Links Faster</b>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('🎓 Dev', url='https://t.me/uni_bypasser)]
        ])
    )

@bot.on_message(regex(r'https?://\S+'))
async def scrape_data(client, message):
    await message.reply_text("Sorry, Bot Is Under Maintenance")

@bot.on_message(command('restart'))
async def restart_bot(client, message):
    restart_message = await message.reply_text('<i>Restarting...</i>')
    await create_subprocess_exec(executable, "python3", "update.py")
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    execl(executable, executable, "-m", "Bypass")

async def check_restart():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f.readline().split())
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text="<i>Restarted !</i>")
        except Exception as e:
            LOGGER.error(e)

async def main():
    bot.add_handler(MessageHandler(
        start, filters=command(BotCommands.StartCommand) & private))
    LOGGER.info("Bypass Bot Started!")
    await bot.start()
    await idle()

if __name__ == "__main__":
    signal(SIGINT, lambda s, f: execl(executable, executable, "-m", "Bypass"))
    bot.loop.run_until_complete(main())
    bot.loop.create_task(check_restart())
    bot.loop.run_forever()
