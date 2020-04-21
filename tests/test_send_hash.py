import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_hash

data = TestData()


@pytest.mark.parametrize('hash', data.data_gen_hash_format(2))
def test_send_ident_generation(hash):
    create_package_to_send_hash(hash)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="idenTest2")
    # send_pack("idenTest2")


@pytest.mark.parametrize('hash', data.data_gen_hash_mutation(1))
def test_send_ident_generation(hash):
    create_package_to_send_hash(hash)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="idenTest2")
