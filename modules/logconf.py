import logging
import datetime

now = datetime.datetime.now()
date_str = now.strftime("%Y-%d-%m_%H%M%S")


def log_for_tests(f_name="file_name", getLog="base_test"):
    logger = logging.getLogger(getLog)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(f"../logs/{f_name}-{date_str}.log", encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
