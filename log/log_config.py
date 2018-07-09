import logging
import logging.handlers
import os

logger = logging.getLogger('jm.server')
formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s ")

DIR_NAME = 'log'
FILE_NAME = 'jm.server.log'

tfh = logging.handlers.TimedRotatingFileHandler(os.path.join(os.path.abspath(DIR_NAME), FILE_NAME), encoding='utf-8', when='d')
tfh.setLevel(logging.DEBUG)
tfh.setFormatter(formatter)

logger.addHandler(tfh)
logger.setLevel(logging.DEBUG)

