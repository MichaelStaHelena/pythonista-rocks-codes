import sys
from loguru import logger

# Remove the default stderr sink and add a clean one for demo output
logger.remove()
logger.add(sys.stdout, format="{level} | {message}", level="DEBUG", colorize=False)

logger.debug("loading config file")          # => DEBUG | loading config file
logger.info("server started on port 8080")   # => INFO | server started on port 8080
logger.warning("disk usage above 80 %")      # => WARNING | disk usage above 80 %

# Structured key=value context — invaluable for searching logs
logger.info("user logged in", extra={"user_id": 42, "ip": "10.0.0.1"})
# => INFO | user logged in

# File rotation in one line (not shown in stdout here, just the API):
# logger.add("app.log", rotation="10 MB", retention="7 days", compression="gz")
