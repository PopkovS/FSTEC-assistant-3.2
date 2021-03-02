from time import sleep

import pytest

from modules.data import TestData
from modules.logconf import log_for_tests
from modules.send_pack_helper import *

data = TestData()

sock = socket.socket()
"""Для этого теста нужно второе корыто у которого ID сервер это ip-адрес устройства 
где запускается тест(192.168.70.101), а порт из "sock.bind(('', 65000))". Перед тестом ведомый должен
запустить у себя скрипт (./run_ass.py) который каждый раз запускает приложение если оно не запущенно
(закрывает приложнеие скрипт с основным тестом)"""


@pytest.fixture(scope="function", autouse=True)
def setup_for_function():
    delete_all_log_file()
    yield
    stop_app()
    assert answer_id_srv_check(), "Не удалось получить ответ от клиета"


@pytest.fixture(scope="module", autouse=True)
def setup():
    print('\n 1111111111111111111')
    sock.bind(('', 65000))
    print('\n 122222111')
    sock.listen(1)
    print('\n 112333333331')
    stop_app()


class TestRecvAuthGen():
    @pytest.fixture(scope="class", autouse=True)
    def setup_gen(self):
        global loggen
        loggen = log_for_tests(f_name="format_gen_recv_auth")

    @pytest.mark.parametrize('access, refresh, expires, email, id', data.data_gen_recv_auth_format(1000))
    def test_recv_auth_format(self, access, refresh, expires, email, id):
        create_package_to_recv_auth(access, refresh, expires, email, id)
        print('\n 22222222222222222222222')
        conn, addr = sock.accept()
        loggen.info(f"Успешное подключение клиента: '{addr}'")
        loggen.debug(f"Подключение с параметрами: {conn}")
        print('\n 33333333333333333333')
        send_func(conn, file_func="func1_2")
        logs_param_recv_auth(access, refresh, expires, email, id)
        loggen.info("Ответ клиенту успешно отправлен")
        conn.close()


class TestRecvAuthMut():
    @pytest.fixture(scope="class", autouse=True)
    def setup_mut(self):
        global logmut
        logmut = log_for_tests(f_name="format_mut_recv_auth")

    @pytest.mark.parametrize('access, refresh, expires, email, id', data.data_gen_recv_auth_mut(1500))
    def test_recv_auth_mut(self, access, refresh, expires, email, id):
        create_package_to_recv_auth(access, refresh, expires, email, id)
        conn, addr = sock.accept()
        logmut.info(f"Успешное подключение клиента: '{addr}'")
        logmut.debug(f"Подключение с параметрами: {conn}")
        send_func(conn, file_func="func1_2")
        logs_param_recv_auth(access, refresh, expires, email, id)
        logmut.info("Ответ клиенту успешно отправлен")


class TestRecvAuthNotFormat():
    @pytest.fixture(scope="class", autouse=True)
    def setup_not_format(self):
        global lognf
        lognf = log_for_tests(f_name="format_not_format_recv_auth")

    @pytest.mark.parametrize('par', ['Access_Token', 'Refresh_Token', 'Expires_in', 'EMail', 'UserID'])
    def test_recv_not_format_without_par(self, par):
        create_package_without(par=par, original_file="func1", new_file="func1_2")
        conn, addr = sock.accept()
        lognf.info(f"Успешное подключение клиента: '{addr}'")
        lognf.debug(f"Подключение с параметрами: {conn}")
        send_func(conn, file_func="func1_2")
        lognf.debug(f"Подготовлен ответ без параметра: {par}")
        lognf.info("Ответ клиенту успешно отправлен")
        conn.close()

    @pytest.mark.parametrize('access', data.data_gen_recv_auth_not_format_access())
    def test_recv_not_format_access(self, access):
        create_package_to_recv_auth(access=access)
        conn, addr = sock.accept()
        lognf.info(f"Успешное подключение клиента: '{addr}'")
        lognf.debug(f"Подключение с параметрами: {conn}")
        send_func(conn, file_func="func1_2")
        logs_param_recv_auth(access)
        lognf.info("Ответ клиенту успешно отправлен")
        conn.close()

    @pytest.mark.parametrize('refresh', data.data_gen_recv_auth_not_format_refresh())
    def test_recv_not_format_refresh(self, refresh):
        create_package_to_recv_auth(refresh=refresh)
        conn, addr = sock.accept()
        lognf.info(f"Успешное подключение клиента: '{addr}'")
        lognf.debug(f"Подключение с параметрами: {conn}")
        send_func(conn, file_func="func1_2")
        logs_param_recv_auth(refresh)
        lognf.info("Ответ клиенту успешно отправлен")
        conn.close()

    @pytest.mark.parametrize('email', data.data_gen_recv_auth_not_format_email())
    def test_recv_not_format_email(self, email):
        create_package_to_recv_auth(email=email)
        conn, addr = sock.accept()
        lognf.info(f"Успешное подключение клиента: '{addr}'")
        lognf.debug(f"Подключение с параметрами: {conn}")
        send_func(conn, file_func="func1_2")
        logs_param_recv_auth(email)
        lognf.info("Ответ клиенту успешно отправлен")
        conn.close()

    @pytest.mark.parametrize('expires, id', data.data_gen_recv_auth_not_format_expires_and_id())
    def test_recv_not_format_expires_and_id(self, expires, id):
        create_package_to_recv_auth(expires=expires, id=id)
        conn, addr = sock.accept()
        lognf.info(f"Успешное подключение клиента: '{addr}'")
        lognf.debug(f"Подключение с параметрами: {conn}")
        send_func(conn, file_func="func1_2")
        logs_param_recv_auth(expires=expires, id=id)
        lognf.info("Ответ клиенту успешно отправлен")
        conn.close()
