import codecs
import re
import socket
import binascii


def sock_connect(ip='192.168.71.03', port=44334, pack_name=""):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    text = open(fr'../packages/{pack_name}', 'rb').read()
    sock.sendall(text)
    print_response(sock)
    return sock


def print_response(sock):
    data = sock.recv(1024).decode("utf-8", errors="replace")
    sock.close()
    print(data)


def recount_length(my_filename="identdata2"):
    with open(f'../packages/{my_filename}') as file_in:
        text = file_in.read()
        text = text.replace(re.search(r'Content-Length: (\d*)\n\n', text).group(1),
                            str(len(re.search(r'Content-Length: \d*\n\n(.*\n.*)', text).group(1))))
        print(len(re.search(r'Content-Length: \d*\n\n(.*\n.*)', text).group(1)))
    write_in_pack(text)


def recount_length_auth():
    with open(r'../packages/auth2', 'r', encoding="utf8", errors='replace') as pack:
        text = pack.read()
        lean = str(len(re.search(r'Content-Length:.\d*\n(\n.*)', text).group(1)))
        with open(r'../packages/auth2', 'rb') as pack:
            text = pack.read()
            text = text.replace(re.search(rb'Content-Length:.(\d*)', text).group(1), lean.encode())
            with open(f"../packages/auth2", "wb") as file_out:
                file_out.write(text)


def create_package_to_send_ident(mac, hs, hv, hn):
    with open('../packages/identdata') as file_in:
        text = file_in.read()
        text = text.replace(re.search(r'M(\w\w-\w\w-\w\w-\w\w-\w\w-\w\w)', text).group(1), mac)
        text = text.replace(re.search(r'HS(\d*)', text).group(1), hs)
        text = text.replace(re.search(r'HV(.*)HN', text).group(1), hv)
        text = text.replace(re.search(r'HN(.*)C', text).group(1), hn)
        text = text.replace(re.search(r'Content-Length: (\d*)\n\n', text).group(1),
                            str(len(re.search(r'Content-Length: \d*\n\n(.*\n.*)', text).group(1))))
    write_in_pack(text)


def create_package_to_send_hash(path, file, hash):
    with open('../packages/identdata') as file_in:
        text = file_in.read()
        text = text.replace(re.search(r'.A.s.s.i.s.t.a.n.t...e.x.e..S.2.5.6..(.+?)..L..', text).group(1), hash)
        text = text.replace(re.search(r'..L..(.+?)..N', text).group(0),
                            b"\x00\x00L\x00\x02\x00".decode("utf8") + path + b"\x00\x03\x00N".decode("utf8"))
        text = text.replace(re.search(r'.N..(.+?)..S.2.5.6.', text).group(1), file)
    write_in_pack(text)


def create_package_to_send_trs(trs, id):
    with open('../packages/trsTest', 'rb') as file_in:
        text = file_in.read()
        text = text.replace(re.search(rb'.{8}(.*).{4}\d{3}\s\d{3}\s\d{3}', text).group(1), trs.encode('cp1251'))
        text = text.replace(re.search(rb'\d{3}\s\d{3}\s\d{3}', text).group(0), id.encode())
        print(text)
    with open(f"../packages/trsTest2", "wb") as file_out:
        file_out.write(text)


def create_package_to_send_auth(login, password):
    with open('../packages/auth', 'rb') as file_in:
        text = file_in.read()
        text = text.replace(re.search(rb'p.1..(.+?)..p.2..', text).group(1), login.encode())
        text = text.replace(re.search(rb'.p.2..(.+?)..p.3.', text).group(1), password.encode())
        text = text.replace(re.search(rb'Content-Length:.(\d*)\r\n\r\n', text).group(1),
                            str(len(re.search(rb'Content-Length:.\d*\r\n\r\n(.*)', text).group(1))).encode())
    with open(f"../packages/auth2", "wb") as file_out:
        file_out.write(text)


def create_package_without(par):
    parameters = {
        r'(.S.2.5.6..+?).L..': "hash",
        r'(..L..+?).N': "path",
        r'(.N..+?).S.2.5.6.': "file",
        r'(M.+?)HS': "mac",
        r'(HS\d*)HV': "hs",
        r'(HV.*)HN': "hv",
        r'(HN.*)CP': "hn"
    }
    for i, j in parameters.items():
        if par == j:
            with open('../packages/identdata') as file_in:
                text = file_in.read()
                text = text.replace(re.search(i, text).group(1), "")
                print(text)
                write_in_pack(text)


def write_in_pack(text, pack="identdata2"):
    try:
        with open(f"../packages/{pack}", "wb") as file_out:
            file_out.write(text.encode("cp1251"))
    except:
        with open(f"../packages/{pack}", "w", encoding='utf-8') as file_out:
            file_out.write(text)

# def



print("+++++++++++++++++++++++++++++++++++++++")
# with open(r'../packages/auth2', 'r', encoding="utf8", errors='replace') as pack:
#     p = pack.read()
#     r = re.search(r'Content-Length:.\d*\n(\n.*)', p).group(1)
#     l = re.search(r'Content-Length:.(\d*)\n\n', p).group(1)


with open(fr'../packages/identdata', 'rb') as pack:
    p = pack.read()
    print(p)
    # r = re.search(rb'Content-Length:.\d*(\r\n\r\n.*)', p).group(1)
    # print(len(r))
    # print(r)
