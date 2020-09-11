import pytest

from modules.base_page import SeleniumHelper
from modules.data import Links, CreteUserPage, TestData
from modules.logconf import log_for_tests

data = TestData()


@pytest.fixture(scope="module")
def browser(browser):
    global page
    page = SeleniumHelper(browser, Links.LOGIN_LINK)
    page.change_sys_paran(dir_control="True")
    page.open()
    page.login(email="test@safib.ru", password="1")
    browser.get(Links.CREATE_USER_LINK_LIN)
    yield page


@pytest.mark.parametrize('email, name, password, phone, comment',
                         data.data_gen_create_user_format(1000))
def test_create_user_format(browser, email, name, password, phone, comment):
    logg = log_for_tests(f_name="format_gen_create_user")
    fields_tuple = email, name, password, password, phone, comment
    logg.debug(f"Переход на форму создания пользователя 'http://lk.3.2-linux.ast.safib.ru/User'")
    logg.info(f"Запуск теста cо следующими значениями полей: {fields_tuple}")
    page.create_user(*fields_tuple)
    page.get_text_alret()
    page.open_page(Links.CREATE_USER_LINK)
    page.check_user_in_bd(email)
    logg.handlers.clear()


@pytest.mark.parametrize('email, name, password, phone, comment',
                         data.data_gen_create_user_mutation(100))
def test_create_user_mutation(browser, email, name, password, phone, comment):
    log = log_for_tests(f_name="mutation_create_user")
    fields_tuple = email, name, password, password, phone, comment
    log.debug(f"Переход на форму создания пользователя 'http://lk.3.4-linux.ast.safib.ru/'")
    log.info(f"Запуск теста cо следующими значениями полей: {fields_tuple}")
    page.create_user(*fields_tuple)
    page.get_text_alret()
    page.open_page(Links.CREATE_USER_LINK)
    page.check_user_in_bd(email)
    log.handlers.clear()


class TestCreateUserNotFormat():
    log = log_for_tests(f_name="not_format_gen_create_user")

    @pytest.mark.parametrize('email', [" ", "testtestmail.ru", "testtest@mailru",
                                       "testtestmailru", "testtestee" * 25 + "@mail.ru"])
    def test_email_field_not_format(self, browser, email):
        self.log.debug(f"Переход на форму создания пользователя 'http://lk.3-4.ast.safib.ru/User'")
        self.log.info(f"Запуск теста c email: '{email}'")
        page.create_user(email=email, name="test_user", password="123", c_password="123")
        page.get_text_alret()
        page.get_text_mess_email(CreteUserPage.ERR_MESS_EMAIL, "email")
        page.open_page(Links.CREATE_USER_LINK)
        page.check_user_in_bd(email)

    @pytest.mark.parametrize('name', [" ", "testtestee" * 26])
    def test_name_field_not_format(self, browser, name):
        self.log.debug(f"Переход на форму создания пользователя 'http://lk.3.4-linux.ast.safib.ru/'")
        self.log.info(f"Запуск теста c name: '{name}'")
        email = "testtest@mail.ru"
        page.create_user(email=email, name=name, password="123", c_password="123")
        page.get_text_alret()
        page.get_text_mess_email(CreteUserPage.ERR_MESS_NAME, "name")
        page.open_page(Links.CREATE_USER_LINK)
        page.clean_aspnetusers(email)
        page.check_user_in_bd(email)

    @pytest.mark.parametrize('passw, c_passw', [(" ", "1qaz@WSX"), ("1qaz@WSX", " "), ("1qaz@WSX", "1qaz@WSX2"),
                                                ("1qa@W", "1qa@W"), ("1qazWSX", "1qazWSX"), ("qaz@WSX", "qaz@WSX"),
                                                ("1QAZ@WSX", "1QAZ@WSX"), ("1qaz@wsx", "1qaz@wsx"),
                                                ("1qaz@WSX" * 17, "1qaz@WSX" * 17)])
    def test_password_field_not_format(self, browser, passw, c_passw):
        page.change_password_setting(6, "True", "True", "True", "True")
        self.log.debug(f"Переход на форму создания пользователя 'http://lk.3-4.ast.safib.ru/User'")
        self.log.info(f"Запуск теста c password: '{passw}' ")
        self.log.info(f"Запуск теста c conf_password: '{c_passw}'")
        email = "testtest@mail.ru"
        page.create_user(email=email, name="test_user", password=passw, c_password=c_passw)
        page.get_text_alret()
        page.get_text_mess_email(CreteUserPage.ERR_MESS_PASS, "password")
        page.open_page(Links.CREATE_USER_LINK)
        page.change_password_setting()
        page.check_user_in_bd(email)
