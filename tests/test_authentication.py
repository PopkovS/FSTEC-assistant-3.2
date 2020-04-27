import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_auth, recount_length_auth

data = TestData()


@pytest.mark.parametrize('login, password', data.data_gen_auth_format(10))
def test_send_pack_auth_generation(login, password):
    print("\n", login.replace(chr(0), ""), len(login.replace(chr(0), "")), sep=" ------ ")
    print("\n", password.replace(chr(0), ""), len(password.replace(chr(0), "")), sep=" ------ ")
    create_package_to_send_auth(login, password)
    recount_length_auth()
    sock_connect(ip="192.168.71.3", port=44334, pack_name="auth2")


@pytest.mark.parametrize('login, password', data.data_gen_auth_mut(13))
def test_send_pack_auth_mut(login, password):
    print("\n", login, len(login), sep=" ------ ")
    print("\n", password, len(login), sep=" ------ ")
    create_package_to_send_auth(login, password)
    recount_length_auth()
    sock_connect(ip="192.168.71.3", port=44334, pack_name="auth2")

@pytest.mark.parametrize('login, password', data.data_gen_auth_not_format())
def test_send_pack_auth_not_format(login, password):
    print("\n", login.replace(chr(0), ""), len(login.replace(chr(0), "")), sep=" ------ ")
    print("\n", password.replace(chr(0), ""), len(password.replace(chr(0), "")), sep=" ------ ")
    create_package_to_send_auth(login, password)
    recount_length_auth()
    sock_connect(ip="192.168.71.3", port=44334, pack_name="auth2")