import sys
import pytest
import time
from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_trs

data = TestData()

start = time.time()

ip_adr = '192.168.70.36'
port = 44444


@pytest.mark.parametrize('trs, id', data.data_gen_trs_format(10))
def test_send_pack_to_trs_format(trs, id):
    print("\n" + id, len(id), sep=" ------ ")
    print("\n" + trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id, original_file="trs_lin", new_file="trs_lin2")
    sock_connect(ip=ip_adr, port=port, pack_name="trs_lin2")
    time.sleep(0.6)


@pytest.mark.parametrize('trs, id', data.data_gen_trs_mut(12200))#12500
def test_send_pack_to_trs_mutation(trs, id):
    print("\n" + id, len(id), sep=" ------ ")
    print("\n" + trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id, original_file="trs_lin", new_file="trs_lin2")
    sock_connect(ip=ip_adr, port=port, pack_name="trs_lin2", get_response=False)
    time.sleep(0.6)


@pytest.mark.parametrize('trs, id', data.data_gen_trs_not_format())
def test_send_pack_to_trs_not_format(trs, id):
    print("\n" + id, len(id), sep=" ------ ")
    print("\n" + trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id, original_file="trs_lin", new_file="trs_lin2")
    sock_connect(ip=ip_adr, port=port, pack_name="trs_lin2")
    time.sleep(0.6)
