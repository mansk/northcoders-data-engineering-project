import logging
def lambda_handler():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.info("hello i'm working")
    print("Nice one")