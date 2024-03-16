from Bypass import bot, LOGGER, Config
from pyrogram import idle
from os import path as ospath, execl
from asyncio import create_subprocess_exec
from sys import executable
from signal import signal, SIGINT

from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.filters import command, private, regex, user
from .helper.bot_commands import BotCommands

async def start(client, message):
    await message.reply_text(
        f'''<b>Hey User !</b>
        
        <b> Universal Bot With Light Weight Functions To Get Your Destination Links Faster</b>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('🎓 Support Group', url='https://t.me/uni_bypasser')]
        ])
    )

@bot.on_message(regex(r'https?://\S+'))
async def scrape_data(client, message):
    await message.reply_text("Sorry, Bot Is Under Maintenance")

@bot.on_message(command('restart') & user(Config.OWNER_ID))
async def restart_command(client, message):
    restart_message = await message.reply('<i>Restarting...</i>')
    await (await create_subprocess_exec('python3', 'update.py')).wait()
    with open(".restartmsg", "w") as f:
        f.write(f"{restart_message.chat.id}\n{restart_message.id}\n")
    execl(executable, executable, "-m", "Bypass")

async def restart():
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
    bot.loop.create_task(restart())
    bot.loop.run_forever()
