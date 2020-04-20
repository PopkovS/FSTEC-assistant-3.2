import re
import socket


def request_sending_edit_user(my_filename='edit_user', id_user='144', email="TestData.USER_AD_NAME", status_id="0",
                              two_factor="False"):
    with open(fr'../packages/{my_filename}.txt', 'rb+') as fp:
        pack_read = fp.read()
        old_id = re.search(r"name=\"Id\"\r\n\r\n(\d*)\r\n", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_id}', f"name=\"Id\"\r\n\r\n{id_user}\r\n", pack_read.decode("utf-8"))

        old_email = re.search(r"name=\"Email\"\r\n\r\n(.*@.*)\r\n", pack_read.decode("utf-8")).group(1)
        new_pack = re.sub(fr'{old_email}', email, new_pack)

        old_status_id = re.search(r"name=\"StatusId\"\r\n\r\n\d", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_status_id}', f"name=\"StatusId\"\r\n\r\n{status_id}", new_pack)

        old_two_factor = re.search(r"name=\"TwoFactor\"\r\n\r\n\w{4,5}", pack_read.decode("utf-8")).group(0)
        new_pack = re.sub(fr'{old_two_factor}', f"name=\"TwoFactor\"\r\n\r\n{two_factor}", new_pack)

        open(fr'../packages/{my_filename}.txt', 'w').close()
        fp.seek(0)
        fp.write(new_pack.encode("utf-8"))


def sock_connect(ip='192.168.71.03', port=44334, pack_name=""):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    sock.sendall(open(rf'../packages/{pack_name}', 'rb').read())
    print_response(sock)
    return sock


def send_pack(pak_name):
    sock = sock_connect()
    sock.sendall(open(rf'../packages/{pak_name}', 'rb').read())
    print_response(sock)


def print_response(sock):
    data = sock.recv(1024).decode("utf-8", errors="replace")
    sock.close()
    print(data)


def recount_length(my_filename):
    with open(fr'../packages/{my_filename}.txt', 'rb+') as fp:
        pack_read = fp.read()
        length_old = re.search(r'Content-Length: (\d*)', pack_read.decode("utf-8")).group(1)
        length_new = len(pack_read[1137:])
        new_pack = re.sub(fr'{length_old}', f'{length_new}', pack_read.decode("utf-8"))
        open(fr'../packages/{my_filename}.txt', 'w').close()
        fp.seek(0)
        fp.write(new_pack.encode("utf-8"))


def create_package_to_send_ident(mac, hs, hv, hn, cp):
    with open('../packages/idenTest') as file_in:
        text = file_in.read()
        text = text.replace(re.search(r'M(\w\w:\w\w:\w\w:\w\w:\w\w:\w\w)', text).group(1), mac)
        text = text.replace(re.search(r'HS(\d*)', text).group(1), hs)
        text = text.replace(re.search(r'HV(.*)HN', text).group(1), hv)
        text = text.replace(re.search(r'HN(.*)C', text).group(1), hn)
        text = text.replace(re.search(r'CP(.*)HN', text).group(1), cp)
        text = text.replace(re.search(r'Content-Length: (\d*)\n\n', text).group(1),
                            str(len(re.search(r'Content-Length: \d*\n\n(.*)', text).group(1))))
    with open("../packages/idenTest2", "w", encoding='utf-8') as file_out:
        file_out.write(text)


with open(fr'../packages/idenTest', 'r') as pack:
    p = pack.read()
    ln = re.search(r'CP(.*)HN', p).group(1)
    # l = re.search(r'Content-Length: \d*\n\n(.*)', p).group(1)
    print(len(ln))
