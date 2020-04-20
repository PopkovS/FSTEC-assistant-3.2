import logging
import os
import re
import string
import sys


def word_count(myfile):
    logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')
    try:
        # считаем слова, логируем результат.
        with open(myfile, 'r') as f:
            file_data = f.read()
            words = file_data.split(" ")
            num_words = len(words)
            logging.debug("this file has %d words", num_words)
            return num_words
    except OSError as e:
        logging.error("error reading the file")

# st = "ss_klklklklklklklk_dd"
# print(re.sub(r'(?<=\s\s)(.*)(_dd)', r'zzzzzzzzzz', st))
# print(string.digits + string.ascii_lowercase)