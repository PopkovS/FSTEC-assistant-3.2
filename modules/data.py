import string

from selenium.webdriver.common.by import By

# from faker import Faker
from modules.generator import gen_rand_sting, create_sequence


class Locators():
    EMAIL_FIELD = (By.CSS_SELECTOR, "#Email[name=\"Email\"]")
    PASSWORD_USER_FIELD = (By.CSS_SELECTOR, "#PasswordUser[name=\"PasswordUser\"]")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, ".btn.btn-primary.block.full-width.m-b")
    USER_MENU = (By.CSS_SELECTOR, ".dropdown-toggle>.uname")


class Menu():
    MENU_FIRST_LEVEL_ADM = (By.XPATH, '//span[text()="Администрирование"]')
    MENU_SECOND_LEVEL_ADM_USR = (By.CSS_SELECTOR, 'li>[href="/User"]')


class Other():
    CREATE_USER_BUT = (By.CSS_SELECTOR, '[title="Создать"]')


class CreteUserPage():
    EMAIL_FIELD = (By.ID, "Email")
    NAME_FIELD = (By.ID, "UserName")
    PASS_FIELD = (By.ID, "Password")
    CONF_PASS_FIELD = (By.ID, "ConfirmPassword")
    PHONE_FIELD = (By.ID, "Phone")
    STAT_SELECT = (By.CSS_SELECTOR, "select#StatusId")
    STAT_OPTIONS = (By.CSS_SELECTOR, "select#StatusId>option")
    TWOFAC_CHECKBOX = (By.ID, "Password")
    COMMENT_FIELD = (By.ID, "Comment")
    NOTIFY_CHECKBOX = (By.ID, "NotifyForSupport")
    TIME_ZONE_SELECT = (By.CSS_SELECTOR, "select#TimeZoneId")
    TIME_ZONE_OPTIONS = (By.CSS_SELECTOR, "select#TimeZoneId>option")
    ROL_ADM_SYS_CHECBOX = (By.ID, "Roles_0__IsChecked")
    ROL_ADM_SECURITY_CHECBOX = (By.ID, "Roles_1__IsChecked")
    SUBMIT = (By.CSS_SELECTOR, '.btn.btn-primary[type="submit"]')
    ALERT_MESS = (By.ID, 'toast-container')
    ERR_MESS = (By.CSS_SELECTOR, '[for="Email"]')


class Links():
    MAIN_LINK = "http://lk.3-2.ast.safib.ru/"
    LOGIN_LINK = MAIN_LINK + "/Account/Login"
    CREATE_USER_LINK = MAIN_LINK + "/User/Create"


class TestData():
    TEST_SYM_SRING = create_sequence((32, 127), (161, 192), (1025, 1026), (1040, 1104), (1105, 1106))

    def data_gen_create_user(self, count):
        test_list = self.TEST_SYM_SRING
        test_data2 = [
            (gen_rand_sting(test_list, (1, 20)) + "@" + gen_rand_sting(test_list, (1, 20)) + "." + gen_rand_sting(
                test_list, (1, 10)),
             gen_rand_sting(test_list, (1, 20)),
             gen_rand_sting(test_list, (1, 20)),
             gen_rand_sting(string.digits, 10),
             gen_rand_sting(test_list, (10, 60)))
            for _ in range(count)]
        return test_data2

