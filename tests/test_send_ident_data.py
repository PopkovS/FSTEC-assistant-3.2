import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_ident

data = TestData()


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_format(1))
def test_send_ident_generation(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="idenTest2")
    # send_pack("idenTest2")


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_mutation(1))
def test_send_ident_mutation(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="idenTest2")


