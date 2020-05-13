import datetime
from time import sleep

import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_ident, create_package_without, recount_length

data = TestData()
now = datetime.datetime.now()
f = data.data_gen_ident_format(10)


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_format(1))
def test_send_ident_format(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn, original_file="ident_lin", new_file="ident_lin2")
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2")


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_mutation(14000))
def test_send_ident_mutation(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn, original_file="ident_lin", new_file="ident_lin2")
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2")
    sleep(0.5)


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_not_format())
def test_send_ident_not_format(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn, original_file="ident_lin", new_file="ident_lin2")
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2")


@pytest.mark.parametrize('par', ["mac", "hs", "hv", "hn"])
def test_send_ident_without_par(par):
    create_package_without(par)
    recount_length()
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2")
