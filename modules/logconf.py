import logging
import datetime

now = datetime.datetime.now()


def logs(file, log_obj):
    now_el = datetime.datetime.now()
    date_str = now_el.strftime("%d-%m-%Y %H:%M")
    logging.basicConfig(level=logging.INFO,
                        filename=f"../logs/{file}-{date_str}.log",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    return logging.getLogger(log_obj)
    # pass