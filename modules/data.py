import random
import string

from selenium.webdriver.common.by import By

# from faker import Faker
from modules.generator import gen_rand_sting, create_sequence, str_in_email, str_in_mac, zzuf


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
    ERR_MESS_EMAIL = (By.CSS_SELECTOR, '[for="Email"]')
    ERR_MESS_NAME = (By.CSS_SELECTOR, '[data-valmsg-for="UserName"]')
    ERR_MESS_PASS = (By.CSS_SELECTOR, '.field-validation-valid.s-error-message')


class Links():
    MAIN_LINK = "http://lk.3-2.ast.safib.ru/"
    LOGIN_LINK = MAIN_LINK + "/Account/Login"
    CREATE_USER_LINK = MAIN_LINK + "/User/Create"


class TestData():
    TEST_SYM_STRING = create_sequence((32, 127), (1025, 1026), (1040, 1104), (1105, 1106))
    TEST_SYM_EMAIL_CORR = create_sequence((65, 91), (97, 123), (48, 58)) + ['-', '.', '_']
    TEST_SYM_MUT = create_sequence((32, 500))
    TEST_SYM_MAC = create_sequence((48, 58), (97, 102))

    def data_gen_create_user_format(self, count):
        sym_list = self.TEST_SYM_STRING
        test_data = [
            (str_in_email(gen_rand_sting(self.TEST_SYM_EMAIL_CORR, (5, 256))),
             gen_rand_sting(sym_list, (1, 256)),
             gen_rand_sting(sym_list, (1, 128)),
             gen_rand_sting(string.digits, 10),
             gen_rand_sting(sym_list + [" "] * 10, (0, 60)))
            for _ in range(count)]
        return test_data

    def data_gen_create_user_mutation(self, count):
        sym_list = self.TEST_SYM_STRING
        sym_mut = self.TEST_SYM_MUT
        test_data = [
            (str_in_email(zzuf(gen_rand_sting(self.TEST_SYM_EMAIL_CORR, (5, 256)), sym_mut, random.randint(1, 100))),
             zzuf(gen_rand_sting(sym_list, (1, 256)), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(sym_list, (1, 128)), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(string.digits, 10), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(sym_list + [" "] * 10, (0, 60)), sym_mut, random.randint(1, 100)))
            for _ in range(count)]
        return test_data

    def data_gen_ident_format(self, count):
        test_data = [
            (str_in_mac(gen_rand_sting(string.hexdigits, 12)),
             gen_rand_sting(string.digits, 11),
             gen_rand_sting(self.TEST_SYM_EMAIL_CORR, 8),#8
             gen_rand_sting(string.digits + string.ascii_letters, 10),#10
             gen_rand_sting(self.TEST_SYM_EMAIL_CORR + [" "] * 10, 77))#77
            for _ in range(count)]
        return test_data

    def data_gen_ident_mutation(self, count):
        sym_mut = self.TEST_SYM_MUT
        test_data = [
            (str_in_mac(zzuf(gen_rand_sting(string.hexdigits, 12), sym_mut, random.randint(1, 100))),
             zzuf(gen_rand_sting(string.digits, 11), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(self.TEST_SYM_EMAIL_CORR, 8), sym_mut, random.randint(1, 100)),#8
             zzuf(gen_rand_sting(string.digits + string.ascii_letters, 10), sym_mut, random.randint(1, 100)),#10
             zzuf(gen_rand_sting(self.TEST_SYM_EMAIL_CORR + [" "] * 10, 77), sym_mut, random.randint(1, 100))) #77
            for _ in range(count)]
        return test_data


c = TestData()
print(c.TEST_SYM_EMAIL_CORR)
[print(i) for i in c.data_gen_ident_mutation(3)]
