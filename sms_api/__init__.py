import logging as log
import logging.config
from os import path

logFile='logging.properties'

f=None
try:
    f = open(logFile)
    log.config.fileConfig(logFile)
    log.raiseExceptions = False
except Exception:
    pass
finally:
    if f:
        f.close()
