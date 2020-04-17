import pytest
from modules.base_page import SeleniumHelper
from modules.data import Locators, Links, Menu, Other, CreteUserPage


def create_sequence(*args):
    sequence = []
    for i in args:
        x, y = i
        sequence = sequence + [chr(i) for i in range(x, y)]
    return sequence


test_list = create_sequence((32, 127), (1025, 1026), (1040, 1104), (1105, 1106))


@pytest.fixture(scope="module")
def browser(browser):
    global page
    page = SeleniumHelper(browser, Links.LOGIN_LINK)
    page.change_sys_paran(dir_control="True")
    page.open()
    print(f"\nСимволы для теста:\n {test_list}")
    page.login(email="test@safib.ru", password="1")
    browser.get(Links.CREATE_USER_LINK)
    yield page


@pytest.mark.parametrize('sym', test_list)
def test_create_user_mutation(browser, sym):
    if sym == "'":
        sym = "\'\'"
    email_str = f"testtest{sym}@mail.ru"
    print(f"\n[{sym}]", end="---")
    page.create_user(email=email_str, password="123", c_password="123", name="test_user")
    page.get_text_alret()
    page.open_page(Links.CREATE_USER_LINK)
    page.check_user_in_bd(email=email_str)
    # print("---------------------------------------------")

    # page.get_text_messages()
