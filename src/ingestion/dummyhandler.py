import logging

logger = logging.getLogger("MyLogger")
logger.setLevel(logging.INFO) 


def dummy_handler(event, context):

    logger.info('hello')
    logger.error('checking for errors')
