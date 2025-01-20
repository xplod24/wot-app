import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename="common_app.log", encoding='utf-8', level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class Colors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_CYAN = '\033[96m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END_C = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


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
        print(f"{Colors.OK_GREEN}{message}{Colors.END_C}")
    elif logLevel == "debug":
        logger.debug(message)
        print(f"{Colors.OK_CYAN}{message}{Colors.END_C}")
    elif logLevel == "warning":
        logger.warning(message)
        print(f"{Colors.WARNING}{message}{Colors.END_C}")
    elif logLevel == "error":
        logger.error(message)
        print(f"{Colors.WARNING}{message}{Colors.END_C}")
    elif logLevel == "critical":
        logger.critical(message)
        print(f"{Colors.FAIL}{message}{Colors.END_C}")
    else:
        logger.critical(f"Unknown level {logLevel}")
        print(f"{Colors.FAIL}{logLevel} - Unknown level {Colors.END_C}")
        raise Exception(f"Unknown level {logLevel}")