import pytest
from modules.base_page import SeleniumHelper
from modules.data import Locators, Links, Menu, Other, CreteUserPage
import modules.pg_data_base as pgdb


def create_sequence(*args):
    sequence = []
    for i in args:
        x, y = i
        sequence = sequence + [chr(i) for i in range(x, y)]
    return sequence


test_list = create_sequence((32, 127), (1025, 1026), (1040, 1104), (1105, 1106))


def print_pretty_list(list_t):
    return [print([j for j in list_t[i:i + 20]]) for i in range(0, len(list_t), 20)]


@pytest.fixture(scope="module")
def browser(browser):
    global page
    page = SeleniumHelper(browser, Links.LOGIN_LINK)
    page.change_sys_paran(dir_control="True")
    page.open()
    print(f"\nСимволы для теста:\n")
    print_pretty_list(test_list)
    page.login(email="test@safib.ru", password="1")
    browser.get(Links.CREATE_USER_LINK)
    yield page
    # result()


def result(name):
    print(f"Список валидных символов для {name}:")
    print_pretty_list(good)
    print(f"Список не валидных символов для {name}:")
    print_pretty_list(bad)
    print("\n*Валидность определятется проверкой наличия записи о пользователе в БД, "
          "посде отправки формы создания пользователя ")


good = []
bad = []


# @pytest.mark.parametrize('sym', test_list)
def test_search_bad_sym_email(browser):
    # for sym in test_list:
    for sym in ["A", "b", "0", "П", "г", "н"]:
        if sym == "'":
            sym = "\'"
        email_str = f"testtest{sym}@mail.ru"
        print(f"\n[{sym}]", end="---")
        page.create_user(email=email_str, password="123", c_password="123", name="test_user")
        page.get_text_alret()
        page.open_page(Links.CREATE_USER_LINK)
        good.append(sym) if pgdb.check_user_exist(email_str) else bad.append(sym)
        page.check_user_in_bd(email=email_str)
    result("email")


def test_search_bad_sym_name(browser):
    for sym in test_list:
        # for sym in ["A","b","0","П","г","н"]:
        if sym == "'":
            sym = "\'"
        name_str = f"test_user_test{sym}"
        email_str = "testtest@mail.ru"
        print(f"\n[{sym}]", end="---")
        page.create_user(email=email_str, password="123", c_password="123", name=name_str)
        page.get_text_alret()
        page.open_page(Links.CREATE_USER_LINK)
        good.append(sym) if pgdb.check_user_exist(email_str) else bad.append(sym)
        page.check_user_in_bd(email=email_str)
    result("name")


def test_search_bad_sym_password(browser):
    for sym in test_list:
        # for sym in ["A","b","0","П","г","н"]:
        if sym == "'":
            sym = "\'"
        pass_str = f"test_password_test{sym}"
        email_str = "testtest@mail.ru"
        print(f"\n[{sym}]", end="---")
        page.create_user(email=email_str, password=pass_str, c_password=pass_str, name="test_name")
        page.get_text_alret()
        page.open_page(Links.CREATE_USER_LINK)
        good.append(sym) if pgdb.check_user_exist(email_str) else bad.append(sym)
        page.check_user_in_bd(email=email_str)
    result("password")


def test_search_bad_sym_phone(browser):
    good_number, bad_number = [], []
    for sym in test_list:
        # for sym in ["A","b","0","1","2","3"]:
        if sym == "'":
            sym = "\'"
        phone_str = f"{sym}123456789"
        email_str = "testtest@mail.ru"
        print(f"\n[{sym}]", end="---")
        page.create_user(email=email_str, password="123", c_password="123", name="test_name", phone=phone_str)
        page.get_text_alret()
        page.open_page(Links.CREATE_USER_LINK)
        good.append(sym) if pgdb.check_user_exist(email_str) else bad.append(sym)

        if page.check_phone():
            good_number.append(sym)
            print(f"Был сохранён номер: {page.check_phone()}")
        else:
            print("Номера нет в БД")
            bad_number.append(sym)
        page.check_user_in_bd(email=email_str)
    print(f"Список символов, при которых номер сохранился в БД:")
    print_pretty_list(good_number)
    print(f"Список символов, при которых номер не сохранился:")
    print_pretty_list(bad_number)
    print("")
    result("phone")


def test_search_bad_sym_comment(browser):
    for sym in test_list:
        # for sym in ["A","b","0","П","г","н"]:
        if sym == "'":
            sym = "\'"
        comment_str = f"test_comment_test{sym}"
        email_str = "testtest@mail.ru"
        print(f"\n[{sym}]", end="---")
        page.create_user(email=email_str, password="123", c_password="123", name="test_name", comment=comment_str)
        page.get_text_alret()
        print(f"Тестовый комментарий:\n'{comment_str}'")
        page.open_page(Links.CREATE_USER_LINK)
        good.append(sym) if pgdb.check_user_exist(email_str) else bad.append(sym)
        page.check_user_in_bd(email=email_str)
    result("comment")


def test_max_lean(browser):
    sym = "a"
    while True:
        email_test = f'test_email@mail.ru'
        text_str = 'q' * 126 + sym
        page.create_user(email=email_test, password="123", c_password="123", name=text_str)
        print(f"\n[{len(text_str)}] - Длинна name")
        page.get_text_alret()
        page.get_text_mess()
        if pgdb.check_user_exist(email_test):
            sym += "a"
            pgdb.del_new_user(email_test)
            page.open_page(Links.CREATE_USER_LINK)
            continue
        else:
            print(f"\n[{len(text_str)}] - Максимально доступная длинна name")
            print(email_test)
            break

def test_max_lean_email(browser):
    sym = "a"
    while True:
        email_test = 'qwertasdfgzxcv' * 10 + sym + '@asdfgh.jk'
        # text_str = 'qwertasdfgzxcvb' * 10 + sym + '@asdfgh.jk'
        page.create_user(email=email_test, password="123", c_password="123", name="text_str")
        print(f"\n[{len(email_test)}] - Длинна name")
        page.get_text_alret()
        if pgdb.check_user_exist(email_test):
            sym += "a"
            pgdb.del_new_user(email_test)
            page.open_page(Links.CREATE_USER_LINK)
            continue
        else:
            print(f"\n[{len(email_test)}] - Максимально доступная длинна email")
            print(email_test)
            break
