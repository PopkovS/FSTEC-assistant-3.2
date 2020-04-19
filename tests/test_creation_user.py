import datetime
from time import sleep

import string
import pytest
from modules.base_page import SeleniumHelper
from modules.generator import zzuf, gen_rand_sting
from modules.data import Locators, Links, Menu, Other, CreteUserPage, TestData
from modules.logconf import log_for_tests
import logging

data = TestData()


@pytest.fixture(scope="module")
def browser(browser):
    global page
    # data = TestData()
    page = SeleniumHelper(browser, Links.LOGIN_LINK)
    page.change_sys_paran(dir_control="True")
    page.open()
    page.login(email="test@safib.ru", password="1")
    browser.get(Links.CREATE_USER_LINK)
    yield page


@pytest.mark.parametrize('email, name, password, phone, comment', data.data_gen_create_user_mutation(2))
def test_create_user_mutation(browser, email, name, password, phone, comment):
    log = log_for_tests(f_name="mutation_test_creat_user")
    print("-------------------------------------------------------------------")
    fields_tuple = email, name, password, password, phone, comment
    log.debug(f"Переход на форму создания пользователя 'http://lk.3-2.ast.safib.ru/User'")
    log.info(f"Запуск теста cо слудующими занчениями полей: {fields_tuple}")
    page.create_user(*fields_tuple)
    page.get_text_alret()
    page.open_page(Links.CREATE_USER_LINK)
    page.check_user_in_bd(email)
    log.handlers.clear()


@pytest.mark.parametrize('email, name, password, phone, comment', data.data_gen_create_user_format(2))
def test_create_user_generation(browser, email, name, password, phone, comment):
    log = log_for_tests(f_name="gen_test_creat_user")
    print("-------------------------------------------------------------------")
    fields_tuple = email, name, password, password, phone, comment
    log.debug(f"Переход на форму создания пользователя 'http://lk.3-2.ast.safib.ru/User'")
    log.info(f"Запуск теста c параметрами: {fields_tuple}")
    page.create_user(*fields_tuple)
    page.get_text_alret()
    page.open_page(Links.CREATE_USER_LINK)
    page.check_user_in_bd(email)
    log.handlers.clear()
