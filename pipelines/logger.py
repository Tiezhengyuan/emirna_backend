import sys
import logging



logger = logging.getLogger(__name__)


fileHandler = logging.FileHandler("logs.txt")

jsonFmt = jsonlogger.JsonFormatter(
    "%(name)s %(asctime)s %(levelname)s %(filename)s %(lineno)s %(process)d %(message)s",
    rename_fields={"levelname": "severity", "asctime": "timestamp"},
    datefmt="%Y-%m-%dT%H:%M:%SZ",
)

stdoutHandler.setFormatter(jsonFmt)
fileHandler.setFormatter(jsonFmt)

logger.addHandler(stdoutHandler)
logger.addHandler(fileHandler)

logger.setLevel(logging.DEBUG)

logger.debug("A debug message")
logger.error("An error message")