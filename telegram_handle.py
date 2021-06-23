from pprint import pprint
import wget
import telebot
import os
os.environ['MOZ_HEADLESS'] = '1'
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
os.makedirs('photos', exist_ok=True)
from config import *
import facebook_poster

# os.system("http://mMvnM5:q58u1L@195.85.194.198:8000")
# os.system("https://mMvnM5:q58u1L@195.85.194.198:8000")

try:
    poster = facebook_poster.Setup()
    bot = telebot.TeleBot(TOKEN, )
    
    
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        # print(message)
        bot.reply_to(message, "Howdy, how are you doing?")
    
    
    @bot.channel_post_handler(content_types=['text'])
    def echo_text(message):
        poster.post_group(facebook_group, message.text)
    
    
    @bot.message_handler(content_types=['photo'])
    @bot.channel_post_handler(
        # func=lambda message: message.chat.id == telegram_group_id,
        content_types=['photo'])
    def echo_photo(message):
        print('channel_id:', message.chat.id, message.chat.id == telegram_channel_id)
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file = wget.download('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path),
                             out=file_info.file_path)
        poster.post_group(facebook_group, message.caption, media=[file])
        # bot.reply_to(message, message.caption)
        bot.send_message(-1001381745215, 'Sent\n'+message.caption)
    
    print('started')
    bot.polling(none_stop=True, )
    # bot.get_updates(limit=4)
    
    # chat = bot.get_chat(telegram_group_id)
except KeyboardInterrupt:
    poster.driver.quit()
    print('Driver Closed')
except Exception as e:
    raise e
