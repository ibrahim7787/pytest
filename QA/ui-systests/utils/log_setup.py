import logging
import os

def get_log_fmt():
    fmt = '%(levelname)s - %(id_prefix)s[%(filename)s:%(lineno)d] %(message)s'
    return fmt


def getLogger(name, level=os.getenv('LOG_LEVEL', False) or 'INFO'):


    # FIXME: needed until callers stop using os.getenv w/ default value of False
    if level == None:
        level = 'INFO'

    fmt = get_log_fmt()

    if os.getenv("LAMBDA_TASK_ROOT"):
        # FIXME: this is what causes the problem of name not working
        logger = logging.getLogger()
        fmt += ' %(aws_request_id)s'
        for h in logger.handlers:
            h.setFormatter(logging.Formatter(fmt))

    else:
        # Local Logging

        logger = logging.getLogger(name)
        if logger.handlers:
            handler = logger.handlers[0]
        else:
            handler = logging.StreamHandler()
            logger.addHandler(handler)

        handler.setFormatter(logging.Formatter(fmt))

    logger.setLevel(getattr(logging, level))
    return logger
