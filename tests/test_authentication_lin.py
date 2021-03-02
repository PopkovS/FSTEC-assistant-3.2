from time import sleep

import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_auth, recount_length_auth

data = TestData()
ip_adr = '192.168.70.36'
port = 44334


@pytest.mark.parametrize('login, password', data.data_gen_auth_format(1000))
def test_send_pack_auth_format(login, password):
    create_package_to_send_auth(login, password, original_file="auth_lin", new_file="auth_lin2")
    sock_connect(ip=ip_adr, port=port, pack_name="auth_lin2")
    sleep(0.5)


@pytest.mark.parametrize('login, password', data.data_gen_auth_mut(14000))  # 14000
def test_send_pack_auth_mut(login, password):
    create_package_to_send_auth(login, password, original_file="auth_lin", new_file="auth_lin2")
    sock_connect(ip=ip_adr, port=port, pack_name="auth_lin2")
    sleep(0.5)


@pytest.mark.parametrize('login, password', data.data_gen_auth_not_format())
def test_send_pack_auth_not_format(login, password):
    print(login)
    print(password)
    create_package_to_send_auth(login=login, password=password, original_file="auth_lin", new_file="auth_lin2")
    recount_length_auth()
    sock_connect(ip=ip_adr, port=port, pack_name="auth_lin2")
