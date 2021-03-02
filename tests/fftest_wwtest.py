import os
import re
import requests
from definitions import ROOT_DIR


def create_package_to_send_hash(path, file, hash, new_file="ident_lin2", original_file="ident_lin"):
    with open(os.path.join(ROOT_DIR, "packages", original_file), 'rb') as file_in:
        text = file_in.read()
        text = text.replace(re.search(rb'.S.2.5.6..(.+?)..L..', text).group(1), hash)
        text = text.replace(re.search(rb'..L..(.+?)..N', text).group(0),
                            b"\x00\x00L\x00\x02\x00" + path + b"\x00\x03\x00N")
        text = text.replace(re.search(rb'.N..(A.+?)..S.2.5.6.', text).group(1),
                            file)
    with open(os.path.join(ROOT_DIR, "packages", new_file), 'wb') as nf:
        nf.write(text)

print(len('b 0 7 c 6 b 3 d 0 f c f 8 7 d 9 7 d 6 b 9 7 7 e a d 3 f 1 0 a 3 9 3 a 8 f d d b 9 2 0 0 7 1 c 6 8 c b 6 a '
          'b 1 f 3 7 3 c 2 5 0 0'.replace(" ", '')))
print(len('A s s i s t a n t . e x e'.replace(" ", '')))

hasht=chr(0).join('b 0 7 c 6 b 3 d 0 f c f 8 7 d 9 7 d 6 b 9 7 7 e a d 3 f 1 0 a 3 9 3 a 8 f d d b 9 2 0 0 7 1 c 6 8 c b 6 a b 1 f 3 7 3 c 2 5 0 0'.replace(" ", ''))
name=chr(0).join('A ss s i s t a n t . e x e'.replace(" ", ''))
p = chr(0).join('9')
create_package_to_send_hash(bytes(p.encode('utf8')), bytes(name.encode('utf8')), bytes(hasht.encode('utf8')))

with open(os.path.join(ROOT_DIR, "packages", "ident_lin"), 'rb') as org:
    origin = org.read()

with open(os.path.join(ROOT_DIR, "packages", "ident_lin2"), 'rb') as t:
    text = t.read()
    print(origin.decode('utf8', errors='replace'),'\n')
    print(text.decode('utf8', errors='replace'),'\n')
    # print(re.search(rb'Content-Length:.\d*\r\n\r\n(.*)', text).group(1))
    body=re.search(rb'Content-Length:.\d*\r\n\r\n(.*)', text).group(1)
    # body = re.search(rb'Content-Length:.\d*\n\n(.*)', text).group(1)

url = 'http://192.168.70.36:44334/api/exec'

r = requests.post(url, data=body)
print(r.request.headers)
print(r.text)
