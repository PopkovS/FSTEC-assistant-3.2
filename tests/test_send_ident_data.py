import datetime
from time import sleep
import socket, re
import string
import pytest
from modules.send_pack_helper import sock_connect, create_package_to_send_ident
from modules.base_page import SeleniumHelper
from modules.generator import zzuf, gen_rand_sting
from modules.data import Locators, Links, Menu, Other, CreteUserPage, TestData
from modules.logconf import log_for_tests
import logging

data = TestData()


@pytest.mark.parametrize('mac, hs, hv, hn, cp', data.data_gen_ident_format(1))
def test_send_ident_generation(mac, hs, hv, hn, cp):
    create_package_to_send_ident(mac, hs, hv, hn, cp)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="idenTest2")
    # send_pack("idenTest2")


@pytest.mark.parametrize('mac, hs, hv, hn, cp', data.data_gen_ident_mutation(1))
def test_send_ident_mutation(mac, hs, hv, hn, cp):
    create_package_to_send_ident(mac, hs, hv, hn, cp)
    sock_connect(ip="192.168.71.3", port=44334, pack_name="idenTest2")


