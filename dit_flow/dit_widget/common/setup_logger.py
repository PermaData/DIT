import logging

loggers = {}


def setup_logger(logger_name, log_file, level=logging.DEBUG):
    global loggers

    formatter = logging.Formatter('%(asctime)s : %(message)s')
    if loggers.get(logger_name):
        logger = loggers.get(logger_name)
    else:
        logger = logging.getLogger(logger_name)
    logger.propogate = False

    if log_file is not None:
        fileHandler = logging.FileHandler(log_file, mode='w')
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)
    logger.addHandler(streamHandler)

    logger.setLevel(level)
    loggers.update(dict(logger_name=logger))
    return logger
