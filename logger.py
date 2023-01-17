
import logging
import sys
from fastapi.logger import logger
from settings import settings


def setup_logging():
    addHandler('root')
    addHandler('uvicorn')
    addHandler('uvicorn.access')
    addHandler('fastapi')
    addHandler(settings.log_name)
    logging.getLogger(settings.log_name).propagate = False

    getLogger().info('Initialised logging level=%s',
                              logging.getLevelName(logger.getEffectiveLevel()))


def addHandler(log_name):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)

    ch.setFormatter(CustomFormatter())
    logger.addHandler(ch)


def getLogger(name: str = None):
    log_name = '.'.join(
        filter(lambda x: x != None, [settings.log_name, name])
    )
    return logging.getLogger(log_name)


# def init_logging(name):
#     global APP_NAME
#     APP_NAME = name

#     logging.getLogger("uvicorn").handlers.clear()
#     logging.getLogger("uvicorn").propagate = True

#     root_logger = logging.getLogger()
#     root_logger.setLevel(logging.DEBUG)

#     filters = [APP_NAME, 'fastapi', 'uvicorn', 'sqlalchemy.engine']

#     for f in filters:
#         ch = logging.StreamHandler(sys.stdout)
#         ch.setLevel(logging.DEBUG)

#         ch.setFormatter(CustomFormatter())
#         ch.addFilter(logging.Filter(f))
#         root_logger.addHandler(ch)

#     logger = getLogger()
#     print('logger: ', logger)
#     logger.info('Initialised logging level=%s',
#                 logging.getLevelName(logger.getEffectiveLevel()))


# def getLogger(name=None):
#     global APP_NAME
#     print('APP_NAME: ', APP_NAME)

#     log_names = filter(lambda x: x != None, [APP_NAME, name])

#     return logging.getLogger('.'.join(log_names))


class CustomFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    # {name} {filename}:{lineno}
    # format = '[{asctime}] {levelname:<8s} {name} {message}'
    format = '[{asctime}] {levelname:<8s} {message}'
    format = '{levelname:<8s} {message} [{name}]'

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, style='{')
        return formatter.format(record)
