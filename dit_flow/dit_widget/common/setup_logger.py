import logging

from dit_flow.constants import RUN_MODE

DEFAULT_LOG_LEVEL = logging.INFO


def setup_logger(logger_name, log_file, log_level=logging.ERROR, mode=RUN_MODE.CLI):

    if not hasattr(logging, 'my_handlers'):
        logging.my_handlers = {}

    formatter = logging.Formatter('%(message)s')
    if mode == RUN_MODE.CLI:
        logger = logging.getLogger('')
    else:
        logger = logging.getLogger(logger_name)
    logger.propogate = False

    if log_file is not None:
        if log_file not in logging.my_handlers.keys():
            fileHandler = logging.FileHandler(log_file, mode='a')
            fileHandler.setFormatter(formatter)
            logger.addHandler(fileHandler)
            logging.my_handlers[log_file] = fileHandler
        else:
            logger.addHandler(logging.my_handlers[log_file])

    logger.setLevel(log_level)
    return logger
