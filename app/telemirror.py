import logging
import time
import requests
import json

from telethon import events
from telethon.sessions import StringSession
from telethon.sync import TelegramClient
from telethon.tl.types import InputMediaPoll, MessageMediaPoll, MessageEntityTextUrl
from telethon.tl.types import MessageEntityTextUrl

from database import Database, MirrorMessage
from settings import (API_HASH, API_ID, MAPPING, CHATS, DB_URL,
                      LIMIT_TO_WAIT, LOG_LEVEL, REMOVE_URLS, SESSION_STRING,
                      TIMEOUT_MIRRORING)
from utils import remove_urls

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(level=LOG_LEVEL)

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
db = Database(DB_URL)


def remove_url_from_message(message):
    message.message = remove_urls(message.message)
    if message.entities is not None:
        for e in message.entities:
            if isinstance(e, MessageEntityTextUrl):
                e.url = remove_urls(e.url)
    return message

def get_url_from_message(message):
    url = ""
    if message.entities is not None:
        for e in message.entities:
            if isinstance(e, MessageEntityTextUrl):
                url = e.url
    return url

def sendMessage(target, message, title, url):
    payload = json.dumps({
        "username": title,
        "content": message.message +"\n"+url,
    })

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    }

    requests.request("POST", target, headers=headers, data=payload)
    print(title)
    print(target)


@client.on(events.NewMessage(chats=CHATS))
async def handler_new_message(event):
    """NewMessage event handler.
    """
    try:
        logger.debug(f'New message from {event.chat_id}:\n{event.message}')
        target = MAPPING.get(event.chat_id)
        if target is None or len(target) < 1:
            logger.warning(
                f'NewMessage. No target channel for {event.chat_id}')
            return
        if REMOVE_URLS:
            event.message = remove_url_from_message(event.message)
        sent = 0
        url = get_url_from_message(event.message)
        chat_from = (await event.get_chat())
        if hasattr(chat_from, 'title'):
            title = chat_from.title
        else :
            title = chat_from.first_name + (" " + chat_from.last_name if chat_from.last_name else "")

        sendMessage(target, event.message, title, url)
        sent += 1
        if sent > LIMIT_TO_WAIT:
            sent = 0
            time.sleep(TIMEOUT_MIRRORING)

    except Exception as e:
        logger.error(e, exc_info=True)

if __name__ == '__main__':
    client.start()
    if client.is_user_authorized():
        me = client.get_me()
        logger.info(f'Connected as {me.username} ({me.phone})')
        client.run_until_disconnected()
    else:
        logger.error('Cannot be authorized')
