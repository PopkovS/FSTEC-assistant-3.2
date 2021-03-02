import datetime
from time import sleep

import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_ident, create_package_without, recount_length

data = TestData()
now = datetime.datetime.now()
f = data.data_gen_ident_format(10)

ip_adr = '192.168.70.38'
port = 44334

'''Каждый новый фстек нужны новые пакеты с идентдатой для lin и win серверов'''


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_format(1000))
def test_send_ident_format(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip=ip_adr, port=port, pack_name="identdata2")


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_mutation(14000))
def test_send_ident_mutation(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip=ip_adr, port=port, pack_name="identdata2")
    sleep(0.6)


@pytest.mark.parametrize('mac, hs, hv, hn', data.data_gen_ident_not_format())
def test_send_ident_not_format(mac, hs, hv, hn):
    create_package_to_send_ident(mac, hs, hv, hn)
    sock_connect(ip=ip_adr, port=port, pack_name="identdata2")


@pytest.mark.parametrize('par', ["mac", "hs", "hv", "hn"])
def test_send_ident_without_par(par):
    create_package_without(par)
    recount_length()
    sock_connect(ip=ip_adr, port=port, pack_name="identdata2")
