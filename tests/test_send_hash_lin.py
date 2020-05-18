from time import sleep

import pytest

from modules.data import TestData
from modules.send_pack_helper import sock_connect, create_package_to_send_hash, recount_length, create_package_without

data = TestData()


@pytest.mark.parametrize('path, file, hash', data.data_gen_hash_format(1000))
def test_send_hash_format(path, file, hash):
    create_package_to_send_hash(path, file, hash, original_file="ident_lin", new_file="ident_lin2")
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2")


@pytest.mark.parametrize('path, file, hash', data.data_gen_hash_mutation(15500)) #15500
def test_send_hash_mutation(path, file, hash):
    create_package_to_send_hash(path, file, hash, original_file="ident_lin", new_file="ident_lin2")
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2")
    sleep(0.5)


@pytest.mark.parametrize('path, file, hash', data.data_gen_hash_not_format())
def test_send_hash_not_format(path, file, hash):
    create_package_to_send_hash(path, file, hash, original_file="ident_lin", new_file="ident_lin2")
    recount_length()
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2", get_response=False)


@pytest.mark.parametrize('par', ["path", "file", "hash"])
def test_send_hash_without_par(par):
    create_package_without(par)
    recount_length()
    sock_connect(ip="192.168.71.50", port=44334, pack_name="ident_lin2")
