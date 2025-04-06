import logging
import sys

# get logger
logger = logging.getLogger()

# make formatter
formatter = logging.Formatter(
    fmt="%(asctime)s - %(levelname)s - %(message)s"
)

# make handler
stream_handler = logging.StreamHandler(sys.stdout)

# set formatter
stream_handler.setFormatter(formatter)

# add handler to logger
logger.handlers = [stream_handler]

logger.setLevel(logging.INFO)
logger.setLevel(logging.ERROR)