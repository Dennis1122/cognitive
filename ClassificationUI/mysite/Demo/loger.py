import logging
import time
import myconfig
from logging.handlers import TimedRotatingFileHandler
logger = logging.getLogger("Rotating Log")
logger.setLevel(myconfig.log_level)
handler = TimedRotatingFileHandler(myconfig.log_file_daily,
                                       when="midnight",
                                       interval=1,
                                       backupCount=5)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
