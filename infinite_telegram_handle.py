import os
import logging
import time

"""
%(pathname)s Full pathname of the source file where the logging call was issued(if available).

%(filename)s Filename portion of pathname.

%(module)s Module (name portion of filename).

%(funcName)s Name of function containing the logging call.

%(lineno)d Source line number where the logging call was issued (if available).
"""
name = 'infinite'
level = 10
logger = logging.getLogger(name)

handler = logging.StreamHandler()
formatter = logging.Formatter('[%(name)s] - %(message)s')
handler.setFormatter(formatter)
streamHandler = logging.FileHandler('infinite.log')
formatter = logging.Formatter('%(asctime)s [%(name)s] - %(message)s', datefmt='%Y-%m-%d:%H:%M:%S')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.addHandler(handler)
logger.setLevel(level)


while 1:
    logger.info('starting telegram')
    os.system('python3.7 telegram_handle.py')

    time.sleep(60)


