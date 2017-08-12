import logging


class Logger(object):
    logger = logging.getLogger('mylogger')

    @classmethod
    def debug(cls, msg):
        cls.logger.debug(msg)

    @classmethod
    def info(cls, msg):
        cls.logger.info(msg)

    @classmethod
    def warn(cls, msg):
        cls.logger.warning(msg)

    @classmethod
    def critical(cls, msg):
        cls.logger.critical(msg)
