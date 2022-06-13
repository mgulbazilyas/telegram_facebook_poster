import logging
import time
from tempfile import mkdtemp
from contextlib import contextmanager
from selenium.webdriver.common.by import By  # noqa
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options

errors = []

class KnownException(Exception):

    def __init__(self,*args, **kwargs):
        super(KnownException, self).__init__()
    pass

def make_error_dict(**kwargs):
    pass

def get_driver(disable_images=True, headless=True, options=None):
    from seleniumwire import webdriver
    # from undetected_chromedriver import ChromeDriverManager
    # import seleniumwire.undetected_chromedriver as uc
    # ChromeDriverManager.installed = True

    if options is None:
        options = get_options(disable_images=disable_images, headless=headless)
    driver = webdriver.Chrome(executable_path="/opt/chromedriver",
                              options=options,
                              )
    errors.clear()
    logger = logging.getLogger(
        'seleniumwire.thirdparty.mitmproxy.server.protocol.http')
    log_error = logger.error
    logger.error = lambda line: [errors.append(line), log_error(line)][1]
    driver.get = get_decorator(driver.get)
    return driver

def get_options(disable_images=False, headless=True):
    options = Options()
    # options.binary_location = '/opt/chrome/chrome'
    headless and options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--disable-application-cache")
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--no-first-run")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    if disable_images:
        options.add_argument("--blink-settings=imagesEnabled=false")
    return options


class ErrorType:
    PROXY_ERROR = "PROXY ERROR"


def get_decorator(get):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        if "Invalid proxy server credentials supplied" in errors:
            raise KnownException(
                type=ErrorType.PROXY_ERROR, desc_or_trace="Invalid proxy server credentials supplied")
        try:
            get(*args, **kwargs)
        except WebDriverException as wde:
            print("got error on driver.get:", wde)
            if "net::ERR_TUNNEL_CONNECTION_FAILED" in str(wde):
                try:
                    get(*args, **kwargs)
                except WebDriverException:
                    raise KnownException(make_error_dict(
                        type=ErrorType.PROXY_ERROR, desc_or_trace="Invalid proxy server credentials supplied"))
            else:
                raise
        if "Invalid proxy server credentials supplied" in errors:
            raise KnownException(make_error_dict(
                type=ErrorType.PROXY_ERROR, desc_or_trace="Invalid proxy server credentials supplied"))
        # print("errors:", errors)
        print(f"load time taken: {time.time() - start_time}")
    return wrapper


def test():
    driver = get_driver()

    driver.get("https://facebook.com")
    driver.save_screenshot("/var/www/html/screenshots/test.png")
    print("Screenshot Saved")
    driver.quit()


if __name__ == '__main__':
    test();