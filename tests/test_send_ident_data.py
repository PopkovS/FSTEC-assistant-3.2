import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_ident, create_package_without, recount_length

data = TestData()


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_format(3))
def test_send_ident_generation(mac, hs, hv, hn):
    print("\n")
    [print(i) for i in [mac, hs, hv, hn]]
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="identdata2")


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_mutation(3))
def test_send_ident_mutation(mac, hs, hv, hn):
    print("\n")
    [print(i) for i in [mac, hs, hv, hn]]
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="identdata2")


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_not_format())
def test_send_ident_not_format(mac, hs, hv, hn):
    print("\n")
    [print(i) for i in [mac, hs, hv, hn]]
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="identdata2")


@pytest.mark.parametrize('par', ["mac", "hs", "hv", "hn"])
def test_send_ident_without_par(par):
    print("\n" + par)
    create_package_without(par)
    recount_length()
    sock_connect(ip="192.168.71.3", port=44334, pack_name="identdata2")
