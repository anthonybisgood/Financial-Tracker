import logging


def getLogger():
    logging.basicConfig(
        filename="../logs/all.log",
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s [%(name)s.%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
    )
    logger = logging.getLogger()
    logger.debug("Logger initialized")
    return logger
