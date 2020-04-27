import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_trs

data = TestData()


@pytest.mark.parametrize('trs, id', data.data_gen_trs_format(10))
def test_send_pack_to_trs_generation(trs, id):
    print("\n", trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id)
    sock_connect(ip="192.168.71.3", port=44444, pack_name="trsTest2")


@pytest.mark.parametrize('trs, id', data.data_gen_trs_mut(5))
def test_send_pack_to_trs_mutation(trs, id):
    print(trs, len(trs), sep=" ------ ")
    create_package_to_send_trs(trs, id)
    sock_connect(ip="192.168.71.3", port=44444, pack_name="trsTest2")


@pytest.mark.parametrize('trs, id', data.data_gen_trs_not_format())
def test_send_pack_to_trs_generation_not_format(trs, id):
    print("\n", f"trs: '{trs}'")
    print("\n", f"id: '{id}'")
    create_package_to_send_trs(trs, id)
    sock_connect(ip="192.168.71.3", port=44444, pack_name="trsTest2")