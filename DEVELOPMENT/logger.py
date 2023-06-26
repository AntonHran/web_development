import logging

log_format: str = '%(asctime)s - [%(levelname)s] - %(name)s - %(funcName)15s(%(lineno)d) - %(message)s'

file_handler = logging.FileHandler('app_errors.logs')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(logging.Formatter(log_format))

file_handler_w = logging.FileHandler('app_info.logs')
file_handler_w.setLevel(logging.DEBUG)
file_handler_w.setFormatter(logging.Formatter(log_format))


def get_logging(name: str) -> logging:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler_w)
    logger.addHandler(file_handler)
    return logger
