import logging
import logging.handlers
import time
import os

'''
日志模块
'''
#localTime = time.strftime("%Y-%m-%d")
log_dir_path = "./"
if not os.path.exists(log_dir_path):
    os.makedirs(log_dir_path)
log_filename = log_dir_path + 'carRunning' + '.log'
logger = logging.getLogger()


def set_logger():
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(process)d-%(threadName)s - '
                                  '%(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s')
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename, maxBytes=10485760, backupCount=5, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


set_logger()
