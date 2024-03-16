from traceback import format_exc
from asyncio import sleep
from aiofiles.os import remove as aioremove
from random import choice as rchoice
from time import time
from re import match as re_match
from Bypass import LOGGER, bot
from Bypass.helper.build_button import ButtonMaker
from pyrogram.types import InputMediaPhoto
from pyrogram.errors import ReplyMarkupInvalid, FloodWait, PeerIdInvalid, ChannelInvalid, RPCError, UserNotParticipant, MessageNotModified, MessageEmpty, PhotoInvalidDimensions, WebpageCurlFailed, MediaEmpty

async def chat_info(channel_id):
    channel_id = str(channel_id).strip()
    if channel_id.startswith('-100'):
        channel_id = int(channel_id)
    elif channel_id.startswith('@'):
        channel_id = channel_id.replace('@', '')
    else:
        return None
    try:
        return await bot.get_chat(channel_id)
    except (PeerIdInvalid, ChannelInvalid) as e:
        LOGGER.error(f"{e.NAME}: {e.MESSAGE} for {channel_id}")
        return None
        
async def deleteMessage(message):
    try:
        await message.delete()
    except Exception as e:
        LOGGER.error(str(e))
        
async def editMessage(message, text, buttons=None, photo=None):
    try:
        if message.media:
            if photo:
                photo = rchoice(config_dict['IMAGES']) if photo == 'IMAGES' else photo
                return await message.edit_media(InputMediaPhoto(photo, text), reply_markup=buttons)
            return await message.edit_caption(caption=text, reply_markup=buttons)
        await message.edit(text=text, disable_web_page_preview=True, reply_markup=buttons)
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await editMessage(message, text, buttons, photo)
    except (MessageNotModified, MessageEmpty):
        pass
    except ReplyMarkupInvalid:
        return await editMessage(message, text, None, photo)
    except Exception as e:
        LOGGER.error(str(e))
        return str(e)
        
async def sendMessage(message, text, buttons=None, photo=None):
    try:
        if photo:
            try:
                if photo == 'IMAGES':
                    photo = rchoice(config_dict['IMAGES'])
                return await message.reply_photo(photo=photo, reply_to_message_id=message.id,
                                                 caption=text, reply_markup=buttons, disable_notification=True)
            except IndexError:
                pass
            except (PhotoInvalidDimensions, WebpageCurlFailed, MediaEmpty):
                des_dir = await download_image_url(photo)
                await sendMessage(message, text, buttons, des_dir)
                await aioremove(des_dir)
                return
            except Exception as e:
                LOGGER.error(format_exc())
        return await message.reply(text=text, quote=True, disable_web_page_preview=True,
                                   disable_notification=True, reply_markup=buttons)
    except FloodWait as f:
        LOGGER.warning(str(f))
        await sleep(f.value * 1.2)
        return await sendMessage(message, text, buttons, photo)
    except ReplyMarkupInvalid:
        return await sendMessage(message, text, None, photo)
    except Exception as e:
        LOGGER.error(format_exc())
        return str(e)


async def forcesub(message, ids, button=None):
    join_button = {}
    _msg = ''
    for channel_id in ids.split():
        chat = await chat_info(channel_id)
        try:
            await chat.get_member(message.from_user.id)
        except UserNotParticipant:
            if username := chat.username:
                invite_link = f"https://t.me/{username}"
            else:
                invite_link = chat.invite_link
            join_button[chat.title] = invite_link
        except RPCError as e:
            LOGGER.error(f"{e.NAME}: {e.MESSAGE} for {channel_id}")
        except Exception as e:
            LOGGER.error(f'{e} for {channel_id}')
    if join_button:
        if button is None:
            button = ButtonMaker()
        _msg = "You haven't joined our channel yet!"
        for key, value in join_button.items():
            button.ubutton(f'Join {key}', value, 'footer')
    return _msg, button


async def user_info(user_id):
    try:
        return await bot.get_users(user_id)
    except Exception:
        return ''
