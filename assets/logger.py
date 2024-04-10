import assets
import logging
import colorlog
import datetime
from logging import handlers


def get_log_filename():
    log_filename = f"{assets.Logs}Log_{datetime.datetime.now().strftime('%Y.%m')}_FL-Bot.log"
    return log_filename


def logger_fun():

    # Konfiguration der Basis-Optionen
    logging.root.setLevel(logging.INFO)
    logging.addLevelName(35, "IMPORTANT")
    logging.addLevelName(11, "CHANNELS")

    # Logger erstellen
    logger = logging.getLogger("Basic_Logger")

    # Konsolen-Logger
    console_handler = colorlog.StreamHandler()
    log_format = ('[%(asctime)s]%(log_color)s %(levelname)s: %(message)s')
    cf = colorlog.ColoredFormatter(fmt=log_format, datefmt='%H:%M:%S %d.%m.%Y', reset=True,
                                   log_colors={'DEBUG': 'cyan',
                                               'INFO': 'green',
                                               'WARNING': 'yellow',
                                               'ERROR': 'red',
                                               'CRITICAL': 'red',
                                               'IMPORTANT': 'blue',
                                               'CHANNELS': 'purple',
                                               'reset': 'white'})
    console_handler.setFormatter(cf)

    # File-Logger
    file_handler = logging.handlers.TimedRotatingFileHandler(get_log_filename(), when="midnight", backupCount=0)
    file_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s] %(levelname)s: %(message)s',
                                                datefmt='%H:%M:%S %d.%m.%Y'))

    # Handler hinzufügen
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
