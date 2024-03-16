from Bypass import bot, LOGGER, Config
from asyncio import create_subprocess_exec
from os import path as ospath, execl
from signal import signal, SIGINT
from .helper.bot_commands import BotCommands
from .helper.message_utils import sendMessage

from pyrogram import Client
from pyrogram.handlers import MessageHandler
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.filters import command, private, regex, user
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

async def is_subscribed(_, __, update):
    if not Config.FORCE_SUB_CHANNEL:
        return True
    user_id = update.from_user.id
    try:
        member = await bot.get_chat_member(chat_id=Config.FORCE_SUB_CHANNEL, user_id=user_id)
    except UserNotParticipant:
        return False

    if member.status not in [ChatMemberStatus.OWNER, ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.MEMBER]:
        return False
    else:
        return True

@bot.on_message(command('start') & private & is_subscribed)
async def start(client, message):
    await message.reply_text(
        f'''<b>Hey User !</b>
        
        <b> Universal Bot With Light Weight Functions To Get Your Destination Links Faster</b>''',
        quote=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('🎓 Support Group', url='https://t.me/uni_bypasser')]
        ])
    )

@bot.on_message(regex(r'https?://\S+') & private & is_subscribed)
async def scrape_data(client, message):
    await sendMessage(message, "Bot Is Under Maintenance")

@bot.on_message(command('start') & private)
async def not_joined(client, message):
    buttons = [
        [
            InlineKeyboardButton(
                "Join Channel",
                url=client.invitelink)
        ]
    ]
    await message.reply(
        text=f"Hello {message.from_user.first_name}\n\n<b>You need to join my Backup Channel to use me\n\nKindly Please join Channel</b>",
        reply_markup=InlineKeyboardMarkup(buttons),
        quote=True,
        disable_web_page_preview=True
    )

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
    LOGGER.info("Bypass Bot Started!")
    await bot.start()
    await bot.idle()

if __name__ == "__main__":
    signal(SIGINT, lambda s, f: execl(executable, executable, "-m", "Bypass"))
    bot.loop.run_until_complete(main())
    bot.loop.create_task(restart())
    bot.loop.run_forever()
