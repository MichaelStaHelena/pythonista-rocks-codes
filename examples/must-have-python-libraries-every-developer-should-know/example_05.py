import sys
from loguru import logger

# loguru ships one pre-configured logger — just remove the default and re-add
# with the format you want.  No Handlers, Formatters, or getLogger() needed.
logger.remove()
logger.add(sys.stdout, format="{level}: {message}", colorize=False)

logger.debug("loading config")              # => DEBUG: loading config
logger.info("server started on port 8080")  # => INFO: server started on port 8080
logger.warning("disk usage above 80 percent")  # => WARNING: disk usage above 80 percent
logger.error("database connection failed")  # => ERROR: database connection failed

# logger.exception() captures the full traceback automatically — no extra args needed
try:
    1 / 0
except ZeroDivisionError:
    logger.exception("caught an error")     # => ERROR: caught an error
                                            # (followed by the full traceback in real output)
