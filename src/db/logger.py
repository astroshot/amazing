# coding=utf-8

import time
from src.config import logging


logger = logging.getLogger(__name__)


def profile(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        cost = (end - start) * 1000
        logger.info("SQL res: %s, %.2fms", res, cost)
        return res

    return wrapper

