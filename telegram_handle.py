import time
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
status = False

try:
    bot = telebot.TeleBot(TOKEN, )
    bot.send_message(-519543356, 'Bot started')
    self = bot
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
        poster = facebook_poster.Setup()
        poster.post_group(facebook_group, message.text)
        poster.driver.quit()
    
    
    @bot.message_handler(content_types=['photo'])
    @bot.channel_post_handler(
        # func=lambda message: message.chat.id == telegram_group_id,
        content_types=['photo'])
    def echo_photo(message):
        
        if status:
            print('channel_id:', message.chat.id, message.chat.id == telegram_channel_id)
            file_id = message.photo[-1].file_id
            file_info = bot.get_file(file_id)
            file = wget.download('https://api.telegram.org/file/bot{0}/{1}'.format(TOKEN, file_info.file_path),
                                 out=file_info.file_path)
            poster = facebook_poster.Setup()
            poster.post_group(facebook_group, message.caption, media=[file])
            # bot.reply_to(message, message.caption)
            bot.send_message(-1001381745215, 'Sent\n' + message.caption)
            time.sleep(10)
            poster.driver.quit()
    
    bot.polling()
    print('started')
    if 1:
        updates = bot.get_updates(offset=(self.last_update_id + 1),
                                  limit=1)
        bot.process_new_updates(updates)
        print(updates)
        print("sleeping 5 sec")
        time.sleep(5)
except KeyboardInterrupt:
    print('Driver Closed')
except Exception as e:
    raise e

