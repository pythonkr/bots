import logging

logger = logging.getLogger('logger')

fileHandler = logging.FileHandler('./log.txt')
streamHandler = logging.StreamHandler()

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)
