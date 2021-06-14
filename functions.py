import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import time
import threading
import tempfile
import itertools as IT
from selenium.webdriver.common.keys import Keys
from sys import platform
import pathlib
scriptDirectory = pathlib.Path().absolute()
if platform == "linux" or platform == "linux2" or platform == "win32":
    enter_button = Keys.CONTROL + '\n'
elif platform == "darwin":
    enter_button = Keys.COMMAND + '\n'

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager




def uniquify(path, sep='-'):
    def name_sequence():
        count = IT.count()
        yield ''
        while True:
            yield '{s}{n:d}'.format(s=sep, n=next(count))

    orig = tempfile._name_sequence
    with tempfile._once_lock:
        tempfile._name_sequence = name_sequence()
        path = os.path.normpath(path)
        dirname, basename = os.path.split(path)
        filename, ext = os.path.splitext(basename)
        fd, filename = tempfile.mkstemp(dir=dirname, prefix=filename, suffix=ext)
        tempfile._name_sequence = orig
    return filename


def get_firefox(user_data_dir=None):
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


    options = webdriver.FirefoxOptions()
    options.headless = True
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    if user_data_dir:
        fp = webdriver.FirefoxProfile(user_data_dir)
    else:
        fp = webdriver.FirefoxProfile()

    fp.set_preference('dom.push.enabled', False)
    fp.set_preference('media.volume_scale', "0.0")
    
    driver = webdriver.Firefox(
        firefox_profile=fp,
        options=options,
        executable_path=GeckoDriverManager().install(),
        log_path='geckodriver.log')
    return driver


def get_webdriver(user_data_dir=None, headless=False):
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.headless = headless
    if user_data_dir:
        chrome_options.add_argument(f'--user-data-dir={scriptDirectory / user_data_dir}')
    driver = Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    return driver


def login(driver, user, passwd):
    if not (user and passwd):
        input("Login and press Enter: ")
        return

    driver.get('https://facebook.com')

    try:
        time.sleep(4)
        driver.find_elements_by_css_selector("[role=dialog] [type=submit]")[-1].click()
        time.sleep(2)
    except: pass
    driver.find_element_by_css_selector('[name="pass"]').clear()
    driver.find_element_by_css_selector('[name="pass"]').send_keys(passwd.strip())
    driver.find_element_by_css_selector('[name="email"]').clear()
    driver.find_element_by_css_selector('[name="email"]').send_keys(user.strip())
    try:
        driver.find_element_by_css_selector('._9ls9').click();time.sleep(2)
    except: pass
    driver.save_screenshot('screenshots/before_login.png')
    driver.find_element_by_xpath('//*[@type="submit"]').click()
    time.sleep(5)
    driver.save_screenshot('screenshots/after_login.png')

def read_config_file(filename='config.txt'):
    config = {}
    if os.path.exists(filename):
        with open(filename, 'r') as stream:
            lines = stream.read().strip().split('\n')
            for line in lines:
                key, value = line.split(':::')
                key = key.strip().lower()
                value = value.strip()
                config[key] = value
        return config
    else:
        raise Exception(f'{filename} does not exist.')


def post_group(driver, link=None, text=None, photos=[]):
        if text is None: return False
        if link is None or link == '': return False
        driver.get(link)

        try:
            time.sleep(1)
            driver.switch_to.alert.accept()
        except:
            pass
        driver.execute_script('window.scrollTo(0,350);')
        time.sleep(5)
        try:
            # in discussion group this will work
            driver.find_element_by_css_selector('[data-pagelet="GroupInlineComposer"] [role=button] ').click()
        except:
            # TODO: for job group
            raise NotImplementedError("Unknown Error")

        # post_selector = '#mount_0_0 > div > div:nth-child(1) > div.rq0escxv.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb > div > div > div.j83agx80.cbu4d94t.d6urw2fd.dp1hu0rb.l9j0dhe7.du4w35lb > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.pfnyh3mw.jifvfom9.gs1a9yip.owycx6da.btwxx1t3.buofh1pr.dp1hu0rb.ka73uehy > div.rq0escxv.l9j0dhe7.du4w35lb.j83agx80.cbu4d94t.g5gj957u.d2edcug0.hpfvmrgz.rj1gh0hx.buofh1pr.dp1hu0rb > div > div > div.j83agx80.cbu4d94t > div > div > div > div > div.rq0escxv.l9j0dhe7.du4w35lb.qmfd67dx.hpfvmrgz.gile2uim.buofh1pr.g5gj957u.aov4n071.oi9244e8.bi6gxh9e.h676nmdw.aghb5jc5 > div:nth-child(1) > div > div > div > div.k4urcfbm.osnr6wyh.kwzhilbh.lhclo0ds.j83agx80 > div:nth-child(1) > div'
        # driver.find_element_by_css_selector(post_selector).click()
        # time.sleep(5)
        # Post = driver.find_element_by_xpath('//*[@name="xhpc_message_text"]')
        # Post.click()
        time.sleep(5)
        write = [i for i in driver.find_elements_by_css_selector('.notranslate._5rpu[contenteditable="true"]')
                 if i.is_displayed()][-1]
        # write.click()
        write.send_keys(text)
        for photo in photos:
            if photo.strip():
                photo = photo.strip()
                driver.find_elements_by_css_selector('[role=dialog] form input[type=file][accept*=image]')[-1].send_keys(os.path.abspath(photo))
                time.sleep(round(os.path.getsize(photo)/2**16, 2))

        time.sleep(5)
        try:
            write = [i for i in driver.find_elements_by_css_selector('[aria-label="Post"][role=button]')
                     if i.is_displayed()][-1]

            write.click()
        except:
            write = [i for i in driver.find_elements_by_css_selector('[aria-label="Pubblica"][role=button]')
                     if i.is_displayed()][-1]

            write.click()

        # write = driver.find_element_by_xpath('//*[@class="notranslate _5rpu"]')
        # write.send_keys(text)

        # gallery_el = driver.find_element_by_css_selector('[name="composer_photo[]"]')
        # files = [os.path.abspath('media/'+i) for i in os.listdir('media')]
        # text = '\n'.join(files)
        #
        # gallery_el.send_keys(text)
        # time.sleep(15*len(files))
        # requests.api.post(post_api_link, data={'post_type': 1,
        #                                        'post_content': text})
        # write.send_keys(Keys.COMMAND+'\n')


def countTinyPairs(a, b, k):
    count = 0
    for i in a:

        for j in b:
            number = int(str(i) + str(j))
            if number < k:
                count += 1
                print(number, k)
            else:
                print(number,k,'not')
    return count

def meanGroups(a):
    means = [sum(i)/len(i) for i in a]
    temp = []
    checked = []
    output = []
    length = len(means)
    for i in range(length):
        if i in checked: continue
        checked.append(i)
        mean = means[i]
        group = [i]
        for j in range(i+1,length):
            if mean== means[j]:
                checked.append(j)
                group.append(j)
        output.append(group)
    return output


def get_phantomjs():
    driver = webdriver.PhantomJS(executable_path='phantomjs.exe')
    
    return driver