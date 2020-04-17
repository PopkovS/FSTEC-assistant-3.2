from time import sleep

import string
import pytest
from modules.base_page import SeleniumHelper
from modules.generator import zzuf, gen_rand_sting
from modules.data import Locators, Links, Menu, Other, CreteUserPage, TestData
from modules.logconf import logs
import logging

data = TestData()

@pytest.fixture(scope="module")
def browser(browser):
    global logger
    logging.basicConfig(level=logging.INFO, filename="teestроророр.log",
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger = logging.getLogger('baseTestMut')
    global page
    page = SeleniumHelper(browser, Links.LOGIN_LINK)
    page.change_sys_paran(dir_control="True")
    page.open()
    page.login(email="test@safib.ru", password="1")
    browser.get(Links.CREATE_USER_LINK)

    yield page


#
# test_data2 = [(zzuf("testtesttesttesttest", test_list),
#                zzuf("testtesttesttesttest", test_list),
#                zzuf("testtesttesttesttest", test_list),
#                zzuf("testtesttesttesttest", test_list))
#               for i in range(100000)]


# @pytest.mark.parametrize('email, name', [test_data, test_data2])
# @pytest.mark.parametrize('email, name', test_data2)

def test_create_user_mutation(browser):
    em = "emailtesttesttest" * 10 + "@mail.ru"
    page.create_user(email=em, password="123", c_password="123", name="name")
    sleep(10)
    page.open_page(Links.CREATE_USER_LINK)
    page.check_user_in_bd(em)


@pytest.mark.parametrize('email, name, password, phone, comment', data.data_gen_create_user(2))
def test_create_user_generation(browser, email, name, password, phone, comment):
    logger.info("Informational message")
    print(email, name, password, phone, comment, sep="\n --")
    page.create_user(email, name, password, password, phone, comment)
    page.open_page(Links.CREATE_USER_LINK)
    page.check_user_in_bd(email)
