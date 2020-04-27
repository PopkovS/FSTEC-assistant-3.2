import logging
import os
import random
import re
import string
import sys

# with open(fr'../packages/identdata', 'rb') as pack:
#     p = pack.read()
#     p =p.replace(re.search(rb'M(.+?)HS', p).group(1), "sdfgsfdsdf".encode("utf8"))
#     print(p)
#     p =p.replace(re.search(rb'M(.+?)HS', p).group(1), b"sdfgsfdsdf")
#     hs = re.search(rb'(HS\d*)HV', p).group(1)
#     hv = re.search(rb'(HV.*)HN', p).group(1)
#     hn = re.search(rb'(HN.*)CP', p).group(1)
#     # print(mac, len(mac), sep="|  ---   ")
#     print(p)
#     print(hs, len(hs), sep="|  ---   ")
#     print(hv, len(hv), sep="|  ---   ")
#     print(hn, len(hn), sep="|  ---   ")

a = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._"

print(a[12:20])