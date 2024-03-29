import codecs
import logging
import re
import os
import socket
# from socket import socket, AF_INET, SOCK_DGRAM
from modules.data import *
from time import sleep

import winrm

from definitions import ROOT_DIR
import binascii


def sock_connect(ip='192.168.70.36', port=44334, pack_name="", get_response=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    text = open(os.path.join(ROOT_DIR, "packages", pack_name), 'rb').read()
    sock.sendall(text)
    if get_response:
        # print_response(sock)
        # sock.recv(1024).decode("utf-8", errors="replace")
        print(sock.recv(1024).decode("utf-8", errors="replace"))
    return sock


def print_response(sock):
    data = sock.recv(1024).decode("utf-8", errors="replace")
    sock.close()


def recount_length(my_filename="identdata2"):
    with open(f'../packages/{my_filename}') as file_in:
        text = file_in.read()
        text = text.replace(re.search(r'Content-Length: (\d*)\n\n', text).group(1),
                            str(len(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1))))
    write_in_pack(text)


def recount_length_auth():
    with open(r'../packages/auth2', 'r', encoding="utf8", errors='replace') as pack:
        text = pack.read()
        lean = str(len(re.search(r'Content-Length:.\d*(\n\n.*)', text).group(1)))
        with open(r'../packages/auth2', 'rb') as pack1:
            text = pack1.read()
            text = text.replace(re.search(rb'Content-Length:.(\d*)', text).group(1), lean.encode())
            with open(f"../packages/auth2", "wb") as file_out:
                file_out.write(text)


def create_package_to_send_ident(mac, hs, hv, hn, new_file="identdata2", original_file="identdata", recount=True):
    with open(os.path.join(ROOT_DIR, "packages", original_file)) as file_in:
        text = file_in.read()
        text = text.replace(re.search(r'M(\w\w-\w\w-\w\w-\w\w-\w\w-\w\w)', text).group(1), mac)
        text = text.replace(re.search(r'HS(\d*)', text).group(1), hs)
        text = text.replace(re.search(r'HV(.*)HN', text).group(1), hv)
        text = text.replace(re.search(r'HN(.*)C', text).group(1), hn)
        if recount:
            print(len(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1)))
            print(re.search(r'Content-Length: (\d*)\n\n', text).group(1))
            text = text.replace(re.search(r'Content-Length: (\d*)\n\n', text).group(1),
                                str(len(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1))))
    write_in_pack(text, pack=new_file)


def create_package_to_send_hash_old(path, file, hash, new_file="identdata2", original_file="identdata"):
    with open(os.path.join(ROOT_DIR, "packages", original_file)) as file_in:
        text = file_in.read()
        print('Кво символов', str(len(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1))), sep=' --- ')

        print('Это хэш ---- ', len(re.search(r'.S.2.5.6..(.+?)..L..', text).group(1)))
        print('Это хэш ---- ', re.search(r'.S.2.5.6..(.+?)..L..', text).group(1))
        text = text.replace(re.search(r'.S.2.5.6..(.+?)..L..', text).group(1), hash)
        print("Это путь ---  ", len(re.search(r'..L..(.+?)..N', text).group(0)))
        text = text.replace(re.search(r'..L..(.+?)..N', text).group(0),
                            b"\x00\x00L\x00\x02\x00".decode("utf8") + path + b"\x00\x03\x00N".decode("utf8"))

        print('Это файл --- ', len(re.search(r'.N..(A.+?)..S.2.5.6.', text).group(1)))
        print('Это файл --- ', (re.search(r'.N..(A.+?)..S.2.5.6.', text).group(1)))
        text = text.replace(re.search(r'.N..(A.+?)..S.2.5.6.', text).group(1),
                            file)
        print(re.search(r'Content-Length: (\d*)\n\n', text).group(1))
        text = text.replace(re.search(r'Content-Length: (\d*)\n\n', text).group(1),
                            str(len(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1))))
        print('Объём после изменений - ', str(len(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1))))
        print(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1))
    with open(os.path.join(ROOT_DIR, "packages", new_file), 'wb') as nf:
        nf.write(text.encode('utf8'))
    # write_in_pack(text, pack=new_file)


def create_package_to_send_hash(path, file, hash, new_file="ident_lin2", original_file="ident_lin"):
    with open(os.path.join(ROOT_DIR, "packages", original_file), 'rb') as file_in:
        text = file_in.read()
        print(len(re.search(rb'.S.2.5.6..(.+?)..L..', text).group(1).decode('utf8').replace(chr(0), '')))
        print(re.search(rb'..L..(.+?)..N', text).group(0).decode('utf8'))
        print(re.search(rb'.N..(A.+?)..S.2.5.6.', text).group(1).decode('utf8'))
        text = text.replace(re.search(rb'.S.2.5.6..(.+?)..L..', text).group(1), hash)
        text = text.replace(re.search(rb'..L..(.+?)..N', text).group(0),
                            b"\x00\x00L\x00\x02\x00" + path + b"\x00\x03\x00N")
        text = text.replace(re.search(rb'.N..(A.+?)..S.2.5.6.', text).group(1),
                            file)
    with open(os.path.join(ROOT_DIR, "packages", new_file), 'wb') as nf:
        nf.write(text)


def create_package_to_send_trs(trs, id, original_file="trsTest", new_file="trsTest2"):
    with open(os.path.join(ROOT_DIR, "packages", original_file), "rb") as file_in:
        text = file_in.read()
        text = text.replace(re.search(rb'.{8}(.*).{4}\d{3}\s\d{3}\s\d{3}', text).group(1),
                            trs.encode("cp1251", "replace"))
        text = text.replace(re.search(rb'\d{3}\s\d{3}\s\d{3}', text).group(0), id.encode())
    with open(os.path.join(ROOT_DIR, "packages", new_file), "wb") as file_out:
        file_out.write(text)


def create_package_to_send_auth(login, password, original_file='auth', new_file="auth2"):
    with open(os.path.join(ROOT_DIR, "packages", original_file), "rb") as file_in:
        text = file_in.read()
        text = text.replace(re.search(rb'p.1..(.+?)..p.2..', text).group(1), login.encode())
        text = text.replace(re.search(rb'.(p.2..+?)..p.3.', text).group(1),
                            b"p\x002\x00\x02\x00" + password.encode())
        # text = text.replace(re.search(rb'Content-Length:.(\d*)\r\n\r\n', text).group(1),
        #                     str(len(re.search(rb'Content-Length:.\d*\r\n\r\n(.*)', text).group(1).decode(errors="replace"))).encode())
    with open(os.path.join(ROOT_DIR, "packages", new_file), "wb") as file_out:
        file_out.write(text)


def create_package_to_recv_auth(access="", refresh="", expires="", email="", id=""):
    with open(os.path.join(ROOT_DIR, "packages", "func1")) as file_in:
        text = file_in.read()
        text = text.replace(re.search(r'.D.2..(.+?)..D.3.', text).group(1), access) if access else text  # 365
        text = text.replace(re.search(r'.D.3..(.+?)..D.4.', text).group(1), refresh) if refresh else text  # 72
        text = text.replace(re.search(r'.D.4..(.+?)..D.5.', text).group(1), expires) if expires else text
        text = text.replace(re.search(r'.D.5..(.+?)..D.6.', text).group(1), email) if email else text
        text = text.replace(re.search(r'.D.6..(.+?)..D.7.', text).group(1), id) if id else text
    write_in_pack(text, pack="func1_2")


def create_package_without(par, original_file='identdata', new_file="identdata2"):
    parameters = {
        r'(.S.2.5.6..+?).L..': "hash",
        r'(..L..+?).N': "path",
        r'(.N..+?).S.2.5.6.': "file",
        r'(M.+?)HS': "mac",
        r'(HS\d*)HV': "hs",
        r'(HV.*)HN': "hv",
        r'(HN.*)CP': "hn",
        r'(.D.2..+?).D.3.': 'Access_Token',
        r'(.D.3..+?).D.4.': 'Refresh_Token',
        r'(.D.4..+?).D.5.': 'Expires_in',
        r'(.D.5..+?).D.6.': 'EMail',
        r'(.D.6..+?)..D.7.': 'UserID'
    }
    for i, j in parameters.items():
        if par == j:
            with open(f'../packages/{original_file}') as file_in:
                text = file_in.read()
                text = text.replace(re.search(i, text).group(1), "")
                write_in_pack(text, pack=new_file)


def write_in_pack(text, pack="identdata2"):
    try:
        with open(f"../packages/{pack}", "wb") as file_out:
            file_out.write(text.encode("cp1251"))
    except:
        with open(f"../packages/{pack}", "w", encoding='utf-8') as file_out:
            file_out.write(text)


# def

def logs_param_recv_auth(access='', refresh='', expires='', email='', id=''):
    loggen = logging.getLogger('base_test.parameters_gen')
    loggen.debug(f"Параметру 'Access_Token' присвоено значение: {access}") if access else None
    loggen.debug(f"Параметру 'Refresh_Token' присвоено значение: {refresh}") if refresh else None
    loggen.debug(f"Параметру 'Expires_in' присвоено значение: {expires}") if expires else None
    loggen.debug(f"Параметру 'EMail' присвоено значение: {email}") if email else None
    loggen.debug(f"Параметру 'UserID' присвоено значение: {id}") if id else None


def send_func(conn, file_func="func1_2"):
    text = open(os.path.join(ROOT_DIR, "packages", file_func), 'rb').read()
    conn.sendall(text)
    sleep(0.5)


def stop_app():
    # sess = winrm.Session('c432varganov', auth=(r'safib\varganov', '1qaz@WSX'), transport='ntlm')
    sess = winrm.Session('win10', auth=(r'win10\admin', '123'), transport='ntlm')
    sess.run_cmd('taskkill /IM assistant.exe /F')


def answer_id_srv_check():
    """Тест считается успешным если в логах будет строка "Answer id-srv for func #1 process done"
    На данный момент проверка закоменчена потому что не фига не получается.
    На тест по формату всегда должен быть положительный ответ,
    остальные тесты на мутацию и не по формату должны быть отрицательными,
    соответственно надо раскомментить другие строки"""

    loggen = logging.getLogger('base_test.answer')
    # sess = winrm.Session('c432varganov', auth=(r'safib\varganov', '1qaz@WSX'), transport='ntlm')
    sess = winrm.Session('win10', auth=(r'win10\admin', '123'), transport='ntlm')
    r = sess.run_cmd('type "C:\Program Files (x86)\Ассистент\log\AstCln*"')
    sleep(1)
    # if "Answer id-srv for func #1 process done" in r.std_out.decode("utf8", "replace"):
    #     loggen.debug('Получено ответ от клиента: "Answer id-srv for func #1 process done"')
    # return True
    # loggen.debug('Получено ответ от клиента: "Answer id-srv for func #1 process done"')
    # return True
    # else:
    loggen.debug('Не удалось получить ответ от клиента')
    return False
    #     loggen.debug('Не удалось получить ответ от клиента')
    #     return False


def delete_all_log_file():
    # sess = winrm.Session('c432varganov', auth=(r'safib\varganov', '1qaz@WSX'), transport='ntlm')
    sess = winrm.Session('win10', auth=(r'win10\admin', '123'), transport='ntlm')
    sess.run_cmd('DEL /F /S /Q /A "C:\Program Files (x86)\Ассистент\log\*"')


if __name__ == '__main__':
    sock_connect('192.168.70.36', 44444, 'trs_lin2', True)
