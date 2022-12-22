
# pip install pymysql
from pymysql import connect


CONN_INFO: dict = {
    'HOST': 'localhost',                    # Адрес хоста базы данных
    'USER': 'root',                         # Имя пользователя, с которого осуществляются изменения в базе
    'PASSWORD': '!2#4%6&8ZxC8&6%4#2!',      # Пароль пользователя
    'PORT': 2280,                           # Порт для подключения к базе данных
    'DATABASE': 'valera_db',                # Название базы данных
}


def get_str(aim_for_str: [tuple, list], need_to_quota: bool) -> str:

    res_str: str = ''
    index: int = 0
    columns: list

    # преобразование строки для записи в бд
    for i in aim_for_str:
        if need_to_quota:
            res_str += '\'' + i + '\''
        else:
            res_str += i
        if not index + 1 == len(aim_for_str):
            res_str += ', '
        index += 1
    return res_str


class DataBase:
    def __init__(self):

        # подключение к БД
        self.__is_connect: bool = False
        self.__db = connect(
            host=CONN_INFO['HOST'],
            user=CONN_INFO['USER'],
            password=CONN_INFO['PASSWORD'],
            port=CONN_INFO['PORT'],
            db=CONN_INFO['DATABASE']
        )
        self.__is_connect = True
        self.__cur = self.__db.cursor()

    def get_columns(self, table: str) -> dict:

        self.__cur_update()

        # получение полной информации по таблицам
        self.__cur.execute("""describe """ + table)
        desc_res = self.__cur.fetchall()
        res: dict = {
            'columns': (),
            'types': (),
            'null': (),
            'keys': (),
            'default': (),
            'extra': ()
        }

        # сохранение информации
        for i in desc_res:
            res['columns'] += (i[0], )
            res['types'] += (i[1], )
            res['null'] += (i[2], )
            res['keys'] += (i[3], )
            res['default'] += (i[4], )
            res['extra'] += (i[5], )
        return res

    def get_values(self, table: str) -> list:

        self.__cur_update()

        # получение данных
        if table == 'bookings':
            self.__cur.execute(
                """select 
                bookings.id, 
                clients.name, 
                price, 
                rooms.number, 
                room_types.title, 
                time_intervals.duration,  
                employees.name
                from bookings 
                join clients on clients.id=bookings.clients_id
                join rooms on rooms.id=bookings.room_id
                join room_types on rooms.room_types_id=room_types.id
                join time_intervals on time_intervals.id=bookings.time_intervals_id
                join employees on employees.id=bookings.employees_id"""
            )
        elif table == 'client_status':
            self.__cur.execute(
                """select 
                id, title, discount
                from client_status
                """
            )
        elif table == 'clients':
            self.__cur.execute(
                """select 
                clients.id, 
                name,
                tNumber,
                email,
                client_status.title
                from clients
                join client_status on client_status.id=clients.client_status_id
                """
            )
        elif table == 'rooms':
            self.__cur.execute(
                """select 
                rooms.id, room_types.title, number, status
                from rooms
                join room_types on rooms.room_types_id=room_types.id
                """
            )
        elif table == 'room_types':
            self.__cur.execute(
                """select 
                id, title, cost_per_hour
                from room_types
                """
            )
        elif table == 'employees':
            self.__cur.execute(
                """select 
                employees.id, name, passport_number, passport_issued, passport_date, address, tNumber, positions.titile
                from employees
                join positions on employees.positions_id=positions.id
                """
            )
        elif table == 'positions':
            self.__cur.execute(
                """select 
                id, titile, salary
                from positions
                """
            )
        elif table == 'time_intervals':
            self.__cur.execute(
                """select 
                id, start_time, duration, end_time
                from time_intervals
                """
            )
        return list(self.__cur.fetchall())

    def get_tables(self) -> tuple:
        self.__cur_update()
        self.__cur.execute("""show tables""")

        # получение таблиц (здесь не используется, с моего проекта осталось)
        desc_res = list(self.__cur.fetchall())
        res: tuple = ()
        for i in desc_res:
            res += (i[0],)
        return res

    def input_value(self, columns: tuple, values: tuple, table: str):
        db_command: str = """INSERT INTO """ + table + """ (""" + get_str(columns, False) + \
                          """) VALUES (""" + get_str(values, True) + ')'
        self.__cur.execute(db_command)
        self.__db.commit()
        self.__cur_update()

    def delete_value(self, row_id: str, table: str):
        db_command: str = """DELETE FROM """ + table + """ WHERE """ + table + """.id=""" + row_id
        self.__cur.execute(db_command)
        self.__db.commit()
        self.__cur_update()

    def update_value(self, columns: tuple, values: tuple, old_id: str, table: str):
        db_command: str = """UPDATE """ + table + """ SET """
        for i in range(0, len(columns)):
            db_command += columns[i] + ' = '
            db_command += '\'' + values[i] + '\''
            if not i + 1 == len(columns):
                db_command += ', '
        db_command += ' WHERE id=' + old_id
        self.__cur.execute(db_command)
        self.__db.commit()
        self.__cur_update()

    def is_connect(self):

        # это было нужно для меня, тебе это снова не нужно
        return self.__is_connect

    def __cur_update(self):

        # обновление курсора, для того, чтобы показать изменения в бд через приложение без его закрытия при
        # обычной смене таблицы (был в таблице client_status, потом внес через workbench изменения, сменил таблицу,
        # чтобы вернуться потом в client_status и показал ему)
        self.__cur.close()
        self.__db.close()
        self.__is_connect = False
        self.__db.connect()
        self.__is_connect = True
        self.__cur = self.__db.cursor()
