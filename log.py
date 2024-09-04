import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="common_app.log", encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger.critical

def addLog(logLevel, message):
    """Add log message to log file

    Args:
        logLevel (levelname): Based on severity of message there are multiple:
        info - Just information level
        debug - Useful for debugging
        warning - Low severity error
        error - Medium severity error
        critical - Maximum severity error
        
        message (string): Message to add to log
    """
    if logLevel == "info":
        logger.info(message)
    elif logLevel == "debug":
        logger.debug(message)
    elif logLevel == "warning":
        logger.warning(message)
    elif logLevel == "error":
        logger.error(message)
    elif logLevel == "critical":
        logger.critical(message)
    else:
        logger.critical(f"Unknown level {logLevel}")
        raise Exception(f"Unknown level {logLevel}")