import logging
import logging.handlers
import os

logger = logging.getLogger('jm.server')
formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s - %(message)s ")

tfh = logging.handlers.TimedRotatingFileHandler('log\\jm.server.log', encoding='utf-8', when='d')
tfh.setLevel(logging.DEBUG)
tfh.setFormatter(formatter)

logger.addHandler(tfh)
logger.setLevel(logging.DEBUG)

