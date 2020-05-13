import os
import re

from definitions import ROOT_DIR

with open(os.path.join(ROOT_DIR, "packages", "auth_lin2"), "rb") as file_in:
    text = file_in.read()
    print(text)
    print(str(len(re.search(rb'Content-Length:.\d*\r\n\r\n(.*)', text).group(1).decode(errors="replace"))).encode())
    print(str(re.search(rb'Content-Length:.\d*\r\n\r\n(.*)', text).group(1).decode(errors="replace")))