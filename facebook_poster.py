# In[1]
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import time
import threading
from selenium.webdriver.common.keys import Keys
import functions
from config import *
os.makedirs('screenshots', exist_ok=True)


class Setup:
    def __init__(self, **kwargs):
        self.post_data = []
        # with open('logininfo.txt', 'r') as file:
        #     lines = file.readlines()
        #     self.__user = lines[0]
        #     self.__passwd = lines[1]
        self.__user   = username
        self.__passwd = password
        
        self.driver = kwargs.get('driver', None)
        if self.driver is None:
            self.do_driver_open()
        


    def do_driver_open(self):
        self.driver = functions.get_phantomjs()#headless=True)
        self.driver.set_window_size(1200, 700)
        self.driver.get("https://www.facebook.com")
        try:
            self.login()
        except Exception as e:
            print(e)
        return self.driver

    def check_login_needed(self) -> bool:
        pass

    def action(self):
        pass
    

        
    def quit(self):
        self.driver.quit()

    def post_group(self, link=None, text=None, media=[]):
        if text is None: return False
        if link is None or link == '': return False

        driver = self.driver

        driver.get(link)

        try:
            time.sleep(1)
            driver.switch_to.alert.accept()
        except:
            pass
        # driver.save_screenshot('screenshots/before_scroll.png')

        driver.execute_script('window.scrollTo(0,350);')
        time.sleep(5)
        # driver.save_screenshot('screenshots/before_posting.png')
        # try:
        #     driver.find_element_by_css_selector('[loggingname="status_tab_selector"]').click();time.sleep(5)
        # except :
        #     Post = driver.find_element_by_xpath('//*[@name="xhpc_message_text"]')
        #     Post.click()
        driver.find_element_by_css_selector('[data-pagelet="GroupInlineComposer"] div[role=button]').click()
        # Post = driver.find_element_by_xpath('//*[@name="xhpc_message_text"]')
        # Post.click()
        
        time.sleep(5)
        write = [i for i in driver.find_elements_by_css_selector('[role="dialog"] .notranslate._5rpu[contenteditable="true"]')
                 if i.is_displayed()][-1]
        write.click()


        # copying text to clipboard
        # pc.copy(text)

        write.send_keys(text)
        # write.send_keys(Keys.CONTROL + 'V')
        time.sleep(5)
        
        for file in media:
            driver.find_element_by_css_selector('[role="dialog"] input[type=file]').send_keys(os.path.abspath(file))
            time.sleep(5)
            
        # write = driver.find_element_by_xpath('//*[@class="notranslate _5rpu"]')
        # write.send_keys(text)

        # gallery_el = driver.find_element_by_css_selector('[name="composer_photo[]"]')
        # files = [os.path.abspath('media/'+i) for i in os.listdir('media')]
        # text = '\n'.join(files)
        #
        # gallery_el.send_keys(text)
        # time.sleep(15*len(files))
        time.sleep(5)
        write = [i for i in driver.find_elements_by_css_selector('[aria-label="Post"][role=button]')
                 if i.is_displayed()][-1]
        write.click()
        # write.send_keys(Keys.COMMAND+'\n')

    def login(self):
        user, passwd = self.__user, self.__passwd
        functions.login(self.driver, user, passwd)
        # self.driver.find_element_by_css_selector('[name="pass"]').click()
        # self.driver.find_element_by_css_selector('[name="pass"]').send_keys(passwd)
        # self.driver.find_element_by_css_selector('[name="email"]').clear()
        # self.driver.find_element_by_css_selector('[name="email"]').send_keys(user)
        # self.driver.find_element_by_xpath('//*[@type="submit"]').click()

        time.sleep(1)

    def __del__(self):
        self.driver.quit()

