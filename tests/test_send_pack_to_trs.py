import sys
import pytest
import time
from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_trs

data = TestData()

start = time.time()


@pytest.mark.parametrize('trs, id', data.data_gen_trs_format(1000))
def test_send_pack_to_trs_format(trs, id):
    print("\n" + id, len(id), sep=" ------ ")
    print("\n" + trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id)
    sock_connect(ip="192.168.71.3", port=44444, pack_name="trsTest2")


@pytest.mark.parametrize('trs, id', data.data_gen_trs_mut(127000))
def test_send_pack_to_trs_mutation(trs, id):
    print("\n" + id, len(id), sep=" ------ ")
    print("\n" + trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id)
    sock_connect(ip="192.168.71.3", port=44444, pack_name="trsTest2")


@pytest.mark.parametrize('trs, id', data.data_gen_trs_not_format())
def test_send_pack_to_trs_not_format(trs, id):
    print("\n" + id, len(id), sep=" ------ ")
    print("\n" + trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id)
    sock_connect(ip="192.168.71.3", port=44444, pack_name="trsTest2")






