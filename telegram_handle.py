import time
from pprint import pprint
import wget

import datastore
import telebot
import os

os.environ['MOZ_HEADLESS'] = '1'
import ssl

ssl._create_default_https_context = ssl._create_unverified_context
os.makedirs('photos', exist_ok=True)
from config import *
import facebook_poster
import api_poster

# os.system("http://mMvnM5:q58u1L@195.85.194.198:8000")
# os.system("https://mMvnM5:q58u1L@195.85.194.198:8000")
status = True
import logging

"""
%(pathname)s Full pathname of the source file where the logging call was issued(if available).

%(filename)s Filename portion of pathname.

%(module)s Module (name portion of filename).

%(funcName)s Name of function containing the logging call.

%(lineno)d Source line number where the logging call was issued (if available).
"""
name = 'telegram_handle'
level = 10
logger = logging.getLogger(name)

handler = logging.StreamHandler()
formatter = logging.Formatter('[%(name)s] - %(message)s')
handler.setFormatter(formatter)
streamHandler = logging.FileHandler('telegram_handle.log')
formatter = logging.Formatter('%(asctime)s [%(name)s] - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(handler)
logger.setLevel(level)

try:
    bot = telebot.TeleBot(TOKEN, )
    bot.send_message(-519543356, 'Bot started')


    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        print(message.chat.id)
        bot.reply_to(message, "Howdy, how are you doing?")


    @bot.message_handler(commands=['stop_bot', ],
                         func=lambda message: message.chat.id in [795743472, 1461841797, -519543356])
    def stop_bot(message):
        global status
        status = False
        bot.reply_to(message, "bot Stopped")


    @bot.message_handler(commands=['start_bot', ],
                         func=lambda message: message.chat.id in [795743472, 1461841797, -519543356])
    def start_bot(message):
        global status
        status = True
        bot.reply_to(message, "bot started")


    @bot.message_handler(commands=['status', ],
                         func=lambda message: message.chat.id in [795743472, 1461841797, -519543356])
    def start_bot(message):
        global status
        if status:
            bot.reply_to(message, "Running")
        else:
            bot.reply_to(message, "stopped")


    @bot.channel_post_handler(content_types=['text'])
    def echo_text(message):
        bot.reply_to(message, "Not Implemented Yet")


    @bot.message_handler(content_types=['photo'])
    @bot.channel_post_handler(
        # func=lambda message: message.chat.id == telegram_group_id,
        content_types=['photo'])
    def echo_photo(message):

        if status:
            print('channel_id:', message.chat.id, message.chat.id == telegram_channel_id)
            file_id = message.photo[-1].file_id
            (datastore.store.add_object(
                {
                    "telegram_id": message.id,
                    "message": message.caption,
                    "images": file_id,
                    "sender_id": message.chat.id,
                }))


    print('started')
    while 1:
        try:

            bot.polling(none_stop=True, )
        except:
            pass
        time.sleep(10)
    # bot.get_updates(limit=4)

    # chat = bot.get_chat(telegram_group_id)
except KeyboardInterrupt:
    print('Driver Closed')
except Exception as e:
    raise e
