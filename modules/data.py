import random
import string

from selenium.webdriver.common.by import By

# from faker import Faker
from modules.generator import gen_rand_sting, create_sequence, str_in_email, str_in_mac, str_in_id, zzuf, \
    create_empty_field_in_list


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
    # SYM_STRING = create_sequence((32, 127), (1025, 1026), (1040, 1104), (1105, 1106))
    SYM_RUS = create_sequence((1025, 1026), (1040, 1104), (1105, 1106))
    SYM_ENG = string.ascii_letters + string.digits + string.punctuation + " "
    SYM_ENG_RUS = string.ascii_letters + string.digits + string.punctuation + " " + SYM_RUS
    SYM_EMAIL_CORR = create_sequence((65, 91), (97, 123), (48, 58)) + '-._'
    SYM_FOR_FILES = create_sequence((65, 91), (97, 123), (48, 58)) + '.!#$%&"*+/-=?^_`{|}~'
    SYM_MUT = create_sequence((32, 500))
    SYM_HEX = string.digits + string.ascii_lowercase[0:6]

    def data_gen_create_user_format(self, count):
        sym_list = self.SYM_ENG_RUS
        test_data = [
            (str_in_email(gen_rand_sting(self.SYM_EMAIL_CORR, (5, 256))),
             gen_rand_sting(sym_list, (1, 256)),
             gen_rand_sting(sym_list, (1, 128)),
             gen_rand_sting(string.digits, 10),
             gen_rand_sting(sym_list + " " * 10, (0, 60)))
            for _ in range(count)]
        return test_data

    def data_gen_create_user_mutation(self, count):
        sym_list = self.SYM_ENG_RUS
        sym_mut = self.SYM_MUT
        test_data = [
            (str_in_email(zzuf(gen_rand_sting(self.SYM_EMAIL_CORR, (5, 256)), sym_mut, random.randint(1, 100))),
             zzuf(gen_rand_sting(sym_list, (1, 256)), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(sym_list, (1, 128)), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(string.digits, 10), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(sym_list + " " * 10, (0, 60)), sym_mut, random.randint(1, 100)))
            for _ in range(count)]
        return test_data

    def data_gen_ident_format(self, count):
        hex = self.SYM_HEX
        test_data = [
            (str_in_mac(gen_rand_sting(hex, 12)),
             gen_rand_sting(string.digits, 12),
             gen_rand_sting(self.SYM_EMAIL_CORR, 11),  # 11
             gen_rand_sting(string.digits + string.ascii_letters, 8))  # 8
            for _ in range(count)]
        return test_data

    def data_gen_ident_not_format(self):
        hex = self.SYM_HEX
        mac = str_in_mac(gen_rand_sting(hex, 12))
        hs = gen_rand_sting(string.digits, 12)
        hv = gen_rand_sting(self.SYM_EMAIL_CORR, 11)
        hn = gen_rand_sting(string.digits + string.ascii_letters, 8)
        test_data = [*create_empty_field_in_list([mac, hs, hv, hn]),
                     (str_in_mac(gen_rand_sting(self.SYM_MUT, 12)), hs, hv, hn),
                     (mac, gen_rand_sting(self.SYM_MUT, 12), hv, hn),
                     (mac, hs, gen_rand_sting(self.SYM_MUT, 11), hn),
                     (mac, hs, hv, gen_rand_sting(self.SYM_MUT, 8))]
        return test_data

    def data_gen_ident_mutation(self, count):
        sym_mut = self.SYM_MUT
        a = False
        test_data = [
            (str_in_mac(zzuf(gen_rand_sting(string.hexdigits, 12), sym_mut, random.randint(1, 100))),
             zzuf(gen_rand_sting(string.digits, 11), sym_mut, random.randint(1, 100)),
             zzuf(gen_rand_sting(self.SYM_EMAIL_CORR, 8), sym_mut, random.randint(1, 100)),  # 8
             zzuf(gen_rand_sting(string.digits + string.ascii_letters, 10), sym_mut, random.randint(1, 100)))  # 10
            for _ in range(count) if a]
        return test_data

    def data_gen_hash_format(self, count):
        test_data = [
            (chr(0).join(gen_rand_sting(self.SYM_FOR_FILES, (1, 10))),  # 1
             chr(0).join(gen_rand_sting(self.SYM_FOR_FILES, 13)),  # 13
             chr(0).join(gen_rand_sting(self.SYM_HEX, 64)))  # 64
            for _ in range(count)]
        return test_data

    def data_gen_hash_not_format(self):
        path = chr(0).join(gen_rand_sting(self.SYM_FOR_FILES, (1, 10)))
        file = chr(0).join(gen_rand_sting(self.SYM_FOR_FILES, 13))
        hash = chr(0).join(gen_rand_sting(self.SYM_HEX, 64))
        test_data = [
            *create_empty_field_in_list([path, file, hash]),
            (chr(0).join(gen_rand_sting('\\/:*?"<>|', (1, 10))), file, hash),
            (path, chr(0).join(gen_rand_sting('\\/:*?"<>|', 13)), hash),
            (path, file, chr(0).join(gen_rand_sting(self.SYM_RUS, 64)))]
        return test_data

    def data_gen_hash_mutation(self, count):
        sym_mut = self.SYM_MUT
        test_data = [
            (zzuf(chr(0).join(gen_rand_sting(self.SYM_FOR_FILES, (1, 10))), sym_mut, random.randint(1, 100)),  # 1
             zzuf(chr(0).join(gen_rand_sting(self.SYM_FOR_FILES, 13)), sym_mut, random.randint(1, 100)),  # 13
             zzuf(chr(0).join(gen_rand_sting(self.SYM_HEX, 64)), sym_mut, random.randint(1, 100)))  # 64
            for _ in range(count)]
        return test_data

    def data_gen_trs_format(self, count):
        test_data = [
            (gen_rand_sting(self.SYM_ENG_RUS, 16),
             str_in_id(gen_rand_sting(string.digits, 9)))
            for _ in range(count)]
        return test_data

    def data_gen_trs_not_format(self):
        test_data = [
            (gen_rand_sting(self.SYM_MUT, random.randint(17, 30)), str_in_id(gen_rand_sting(string.digits, 9))),
            (gen_rand_sting(self.SYM_MUT, 16), gen_rand_sting(string.digits, 9)),
            (gen_rand_sting(self.SYM_MUT, 16), str_in_id(gen_rand_sting(string.digits, random.randint(10, 15)))),
            (gen_rand_sting(self.SYM_MUT, 16), gen_rand_sting(string.ascii_letters, 9)),
            (gen_rand_sting(self.SYM_MUT, 16), ""),
            ("", str_in_id(gen_rand_sting(string.digits, 9)))
        ]
        return test_data

    def data_gen_trs_mut(self, count):
        sym_mut = self.SYM_MUT
        test_data = [
            (zzuf(gen_rand_sting(self.SYM_MUT, 16), sym_mut, random.randint(1, 100)),
             str_in_id(zzuf(gen_rand_sting(string.digits, 9), sym_mut, random.randint(1, 100))))
            for _ in range(count)]
        return test_data

    def data_gen_auth_format(self, count):
        test_data = [
            (chr(0).join(str_in_email(gen_rand_sting(self.SYM_EMAIL_CORR, 15))),
             chr(0).join(gen_rand_sting(self.SYM_ENG_RUS, 8)))
            for _ in range(count)]
        return test_data

    def data_gen_auth_not_format(self):
        test_data = [
            ("securityasta.ru", "security"),
            ("security@aastru", "security"),
            ("@astaaaaaaaa.ru", "security"),
            ("securityaaaaaa@", "security"),
            ("security@astaa.", "security"),
            ("securitysecurity@ast.ru", ""),
            ("security@asД.ru", "security"),
            ("securitД@ast.ru", "security"),
            ("security@ast.ru" * 18, "security"),
            ("security@ast.ru", "security" * 18),
            ("security@ast.ru", "securit" + chr(181))
        ]
        return test_data

    def data_gen_auth_mut(self, count):
        test_data = [
            (" ".join(zzuf("security@ast.ru", self.SYM_MUT, random.randint(1, 100))),
             " ".join(zzuf("security", self.SYM_MUT, random.randint(1, 100))))
            for _ in range(count)]
        return test_data


c = TestData()
# [print(i) for i in c.data_gen_auth_format(4)]
