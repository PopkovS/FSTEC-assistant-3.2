import psycopg2


# from pages.locators import LoginLocators, Links, TestData


# assistant-test-v3.2F_corp_core
# def db_connect(dbname='assistant_test_corp_linux', user='postgres',
#                password='1q2w3e', host='192.168.70.220'):
def db_connect(dbname='assistant_test_v3.2F_corp_core', user='postgres',
               password='1q2w3e', host='192.168.70.220'):
    conn = psycopg2.connect(dbname=dbname, user=user,
                            password=password, host=host)
    cursor = conn.cursor()
    return conn, cursor


def db_disconnect():
    conn, cursor = db_connect()
    conn.close()
    cursor.close()


def check_user_exist(user):
    conn, cursor = db_connect()
    cursor.execute('SELECT email '
                   'FROM public.astusers'
                   f' WHERE email=$${user}$$')
    astusers = bool(cursor.fetchall())
    cursor.execute(f'SELECT "Email" '
                   f'FROM public."AspNetUsers" '
                   f"WHERE \"Email\" = $${user}$$")
    aspNetUsers = bool(cursor.fetchall())
    assert astusers == aspNetUsers, f"Ответ от таблиц отличается. " \
                                    f"astusers = '{astusers}', AspNetUsers = '{aspNetUsers}'"
    db_disconnect()
    return astusers and aspNetUsers


def check_user_binding_with_ad(user):
    assert check_user_exist(user), f'Не возможно проверить статус привязки пользователя к AD, ' \
                                   f'email "{user}" отсутствует в базе'
    objectguid = get_cell(search_row="objectguid", table="astusers", where_col="email",
                          val=user)
    distinguishedname = get_cell(search_row="distinguishedname", table="astusers", where_col="email",
                                 val=user)
    assert bool(objectguid) == bool(distinguishedname), f'Отличаются наполнение в ячейках: \n' \
                                                        f'objectguid = {bool(objectguid)}\n' \
                                                        f'distinguishedname = {bool(distinguishedname)}'
    db_disconnect()
    return bool(objectguid) and bool(distinguishedname)


def unbinding_user_from_ad(user):
    if check_user_binding_with_ad(user):
        change_cells(table="astusers", column="objectguid", new_val="", where_col="email", where_val=user)
        change_cells(table="astusers", column="distinguishedname", new_val="", where_col="email", where_val=user)
        assert not check_user_binding_with_ad(user), \
            f'Неплоучилось отвязать пользователя "{user}" от AD что то пошло не так'
        db_disconnect()


def get_id_user(user):
    conn, cursor = db_connect()
    assert check_user_exist(user), f"Невозможно получить id, Пользователя {user} нет в базе"
    cursor.execute('SELECT id '
                   'FROM public.astusers'
                   f' WHERE email=$${user}$$')
    result = cursor.fetchall()
    if result:
        return result[0][0]
    db_disconnect()


def change_cells(table, column, new_val, where_col="email", where_val=""):
    conn, cursor = db_connect()
    cursor.execute(f'UPDATE public.{table}'
                   f' SET {column} = \'{new_val}\''
                   f' WHERE {where_col} =\'{where_val}\'')
    conn.commit()
    db_disconnect()


def get_cell(search_row="id", table="astusers", where_col="email", val=''):
    conn, cursor = db_connect()
    cursor.execute(f'SELECT {search_row} '
                   f'FROM public.{table}'
                   f' WHERE {where_col}=\'{val}\'')
    cell = cursor.fetchall()[0][0]
    return cell


def delete_row(table="astclientdevices", column="title", val="'Наименование'"):
    conn, cursor = db_connect()
    cursor.execute(f"DELETE FROM public.{table} WHERE {column} ={val}")
    conn.commit()
    db_disconnect()


def change_stausid(stat=0, user=''):
    stat = int(stat)
    assert check_user_exist(user), f"Невозможно изменить данные, Пользователя {user} нет в базе"
    change_cells(table="astusers", column="status", new_val=stat, where_val=user)
    change_cells(table="\"AspNetUsers\"", column="\"Status\"", new_val=stat, where_col="\"Email\"", where_val=user)
    db_disconnect()


def change_direct_control(val="True"):
    change_cells(table="systemparameters", column="value", new_val=val, where_col="type", where_val=118)
    db_disconnect()


def change_auth_ad(val="True"):
    change_cells(table="systemparameters", column="value", new_val=val, where_col="type", where_val=135)
    if val == "True":
        change_cells(table="systemparameters", column="value", new_val="test.local;safib.ru;test2.test1.local",
                     where_col="type", where_val=136)
    else:
        change_cells(table="systemparameters", column="value", new_val="", where_col="type", where_val=136)
    db_disconnect()


def change_twofactor(val="true", user=""):
    assert check_user_exist(), f"Невозможно изменить данные, Пользователя {user} нет в базе"
    change_cells(table="astusers", column="twofactorsignneeded", new_val=val)
    change_cells(table='"AspNetUsers"', column='"TwoFactorEnabled"', new_val=val, where_col='"Email"',
                 where_val=user)
    db_disconnect()


def del_new_user(user):
    assert check_user_exist(user), f"Пользователя '{user}' нет в бд, удаление не возможно"
    id = get_id_user(user=f'{user}')
    delete_row(table='astclientdevicegroups', column='userid',
               val=(f"'{id}'"))
    delete_row(table='"AspNetUsers"', column='"Email"', val=(f"'{user}'"))
    delete_row(table='astusers', column='email', val=(f"'{user}'"))
    db_disconnect()


def change_password_param(pas_len=1, one_sym="False", one_dig="False", one_lower="False", one_upper="False"):
    change_cells(table="systemparameters", column="value", new_val=pas_len, where_col="type", where_val=120)
    change_cells(table="systemparameters", column="value", new_val=one_sym, where_col="type", where_val=121)
    change_cells(table="systemparameters", column="value", new_val=one_dig, where_col="type", where_val=122)
    change_cells(table="systemparameters", column="value", new_val=one_lower, where_col="type", where_val=123)
    change_cells(table="systemparameters", column="value", new_val=one_upper, where_col="type", where_val=124)
    db_disconnect()
