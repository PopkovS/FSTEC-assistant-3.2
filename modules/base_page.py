import logging
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import modules.pg_data_base as pgdb
from modules.data import Locators, Links, Menu, Other, CreteUserPage

main_link = "http://lk.corp.ast.safib.ru/"


class SeleniumHelper():
    def __init__(self, browser, url, timeout=3):
        self.browser = browser
        self.url = url
        self.browser.implicitly_wait(timeout)

    def open(self):
        self.browser.get(self.url)

    def open_page(self, link):
        self.browser.get(link)

    def is_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.visibility_of_element_located((how, what)))
            # WebDriverWait(self.browser, timeout).until(EC.element_to_be_clickable((how, what)))
        except TimeoutException:
            return False
        return True

    def is_not_element_present(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout).until(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return True

        return False

    def is_disappeared(self, how, what, timeout=4):
        try:
            WebDriverWait(self.browser, timeout, 1, TimeoutException). \
                until_not(EC.presence_of_element_located((how, what)))
        except TimeoutException:
            return False
        return True

    def login(self, email, password, name_user="test@safib.ru"):
        email_field = self.browser.find_element(*Locators.EMAIL_FIELD)
        email_field.send_keys(email)
        password_field = self.browser.find_element(*Locators.PASSWORD_USER_FIELD)
        password_field.send_keys(password)
        submit = self.browser.find_element(*Locators.SUBMIT_BUTTON)
        submit.click()
        assert self.is_element_present(*Locators.USER_MENU,
                                       timeout=8), "Не удалось найти ссылку c именем пользователя на " \
                                                   "странице"
        text_user_name = self.browser.find_element(*Locators.USER_MENU).text
        assert text_user_name == name_user, f"Фактическое имя пользователя авторизованного на сайте '{text_user_name}' " \
                                            f"не совпадает с ожидаемым '{name_user}' "

    def go_to_adm_user(self):
        current_link = self.browser.current_url
        if Links.LOGIN_LINK in current_link:
            self.change_sys_paran(auth_ad="False")
            self.browser.refresh()
            self.login(email="security@ast.ru", password="1")
        else:
            self.browser.refresh()
        self.change_sys_paran(dir_control="True")
        self.open_adm_user_page()

    def open_adm_user_page(self):
        adm_button = self.browser.find_element(*Menu.MENU_FIRST_LEVEL_ADM)
        None if self.is_element_present(*Menu.MENU_SECOND_LEVEL_ADM_USR, timeout=1) else adm_button.click()
        user_button = self.browser.find_element(*Menu.MENU_SECOND_LEVEL_ADM_USR)
        user_button.click()

    def open_create_user_page(self):
        create_butt = self.browser.find_element(*Other.CREATE_USER_BUT)
        create_butt.click()

    def change_sys_paran(self, auth_ad="False", dir_control="False"):
        pgdb.change_auth_ad(auth_ad)
        pgdb.change_direct_control(dir_control)

    def create_sequence(*args):
        sequence = []
        for i in args:
            x, y = i
            sequence = sequence + [chr(i) for i in range(x, y)]
        return sequence

    def create_user(self, email='', name='', password='', c_password='', phone='', comment=''):
        # mylogger = logging.getLogger('baseCreateUser')

        fields = {
            "email": (self.browser.find_element(*CreteUserPage.EMAIL_FIELD), email),
            "name": (self.browser.find_element(*CreteUserPage.NAME_FIELD), name),
            "password": (self.browser.find_element(*CreteUserPage.PASS_FIELD), password),
            "conf password": (self.browser.find_element(*CreteUserPage.CONF_PASS_FIELD), c_password),
            "phone": (self.browser.find_element(*CreteUserPage.PHONE_FIELD), phone),
            "comment": (self.browser.find_element(*CreteUserPage.COMMENT_FIELD), comment)
        }
        for field, val in fields.items():
            if val[1]:
                val[0].clear()
                val[0].send_keys(val[1])
            else:
                continue
        submit_but = self.browser.find_element(*CreteUserPage.SUBMIT)
        submit_but.click()

        # self.browser.get(Links.CREATE_USER_LINK)

    def check_user_in_bd(self, email):
        if email:
            if pgdb.check_user_exist(email):
                pgdb.del_new_user(email)
                print(f'Пользователь: "{email}" успешно создан')
                # assert False, f'Пользователь: "{email}" успешно создан. Сообщение на сайте: "{alr}"'
            else:
                print(f'Пользователь: "{email}" не был создан')
                # assert False, f'Пользователь: "{email}" не был создан по причине: "{alr}"'
        else:
            print("Поле email не было заполнено")

    def get_text_alret(self):
        if self.is_element_present(*CreteUserPage.ALERT_MESS):
            alerts = self.browser.find_elements(*CreteUserPage.ALERT_MESS)
            # [print(f"Сообщение на странице формы cоздания пользователя:\n '{i.text}'") for i in alerts]
            print(f'Сообщение на сайте: {", ".join([i.text for i in alerts])}')

    def get_text_mess(self):
        if self.is_element_present(*CreteUserPage.ERR_MESS, timeout=1):
            err_mes = self.browser.find_element(*CreteUserPage.ERR_MESS)
            return err_mes.text

    def asasa(self):
        return [i*10 for i in range(10)]

