from logging import NullHandler, getLogger

logger = getLogger("phantom_communicator")
logger.addHandler(NullHandler())
