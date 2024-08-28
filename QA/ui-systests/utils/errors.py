import os, json
import traceback as tb
from utils.log_setup import getLogger
from functools import wraps
import inspect

log_level = os.getenv('LOG_LEVEL')
logger = getLogger(__name__, log_level)


def decor_handle_exc(func):
    @wraps(func)
    def with_try(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            msg = f"failed @ File: {inspect.stack()[1].filename} Fuction: {func.__name__} \n{e}"
            handle_exc(msg)

    return with_try


class TestError(Exception):
    def __init__(self, message):
        self.message = message


def handle_exc(msg):
    trace = tb.format_exc()

    if os.getenv('CLOUD_MODE'):
        logger.error(json.dumps({"message": msg, "trace": trace.replace("\n", "\r")}, indent=4))
    else:
        logger.error(msg + trace)

    # Use ENV variable for now
    os.environ['FAILURE_STATUS'] = msg + trace

    raise TestError(msg)
