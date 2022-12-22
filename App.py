
# pip install customtkinter
from customtkinter import CTk, CTkFrame, CTkRadioButton, CTkLabel, CTkEntry, CTkButton, CTkComboBox

from tkinter.ttk import Treeview
from tkinter import messagebox as mb, IntVar

from pymysql import DatabaseError

from DataBase import DataBase


class App:

    def __init__(self):
        try:
            self.__window: DBWindow = DBWindow()
        except DatabaseError:
            mb.showerror('Something went wrong...', 'Database is not reachable now!')

    def exec(self):
        self.__window.mainloop()


class DBWindow(CTk):

    def __init__(self):
        print('Initializing')
        super().__init__()
        self.title('DataBase')

        # ===================Инициализация===================

        # -------------Экранные формы-контейнеры--------------

        self.__table_frame: CTkFrame = CTkFrame(self, height=600, width=1350)
        self.__table_frame.pack_propagate(False)

        self.__quit_frame: CTkFrame = CTkFrame(self)
        self.__update_buttons_frame: CTkFrame = CTkFrame(self, height=50)
        self.__update_entries_frame: CTkFrame = CTkFrame(self, height=50)
        self.__radio_buttons_frame: CTkFrame = CTkFrame(self)

        # ----------------------Таблица-----------------------

        self.__table: Treeview = Treeview(self.__table_frame, selectmode='extended', show='headings', height=600)

        # ----------------------Кнопки------------------------

        self.__quit_button: CTkButton = CTkButton(self.__quit_frame, text='В\nы\nй\nт\nи', height=700, width=50,
                                                  font=('Arial Black', 16), command=self.__quit_click)
        self.__delete_button: CTkButton = CTkButton(self.__update_buttons_frame, text='Удалить', height=50, width=300,
                                                    font=('Arial Black', 16), fg_color='red',
                                                    command=self.__delete_click)
        self.__update_button: CTkButton = CTkButton(self.__update_buttons_frame, text='Обновить', height=50, width=300,
                                                    font=('Arial Black', 16), command=self.__update_click)
        self.__add_button: CTkButton = CTkButton(self.__update_buttons_frame, text='Добавить', height=50, width=300,
                                                 font=('Arial Black', 16), command=self.__insert_click)

        # ----------------------Надписи----------------------

        self.__input_label: CTkLabel = CTkLabel(self.__update_entries_frame, text='Введите данные',
                                                font=('Arial Black', 14))

        # --------------------Переменные---------------------

        self.__db: DataBase = DataBase()
        self.__combo_values: dict = {}
        self.__update_combo_values()
        self.__dict_of_entries: dict = {
            'room_types': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12))
            ],
            'rooms': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=self.__combo_values['rooms']['names']),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12))
            ],
            'client_status': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12))
            ],
            'clients': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=self.__combo_values['clients']['names'])
            ],
            'positions': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12))
            ],
            'employees': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=self.__combo_values['employees']['names'])
            ],
            'time_intervals': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12))
            ],
            'bookings': [
                CTkEntry(self.__update_entries_frame, width=50, font=('Arial Black', 12)),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=self.__combo_values['bookings']['clients']['names']),
                CTkEntry(self.__update_entries_frame, width=150, font=('Arial Black', 12)),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=self.__combo_values['bookings']['rooms']['names'],
                            command=self.__validate_booking_room_types_combobox),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=[]),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=self.__combo_values['bookings']['time_intervals']['names']),
                CTkComboBox(self.__update_entries_frame, font=('Arial Black', 12),
                            values=self.__combo_values['bookings']['employees']['names'])
            ]
        }
        self.__update_combo_boxes_values()
        self.__dict_of_labels: dict = {
            'room_types': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Title', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Cost/hour', font=('Arial Black', 12))
            ],
            'rooms': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Room Type', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Number', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Status', font=('Arial Black', 12))
            ],
            'client_status': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Title', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Discount', font=('Arial Black', 12))
            ],
            'clients': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Name', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Phone Number', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Email', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Status', font=('Arial Black', 12))
            ],
            'positions': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Title', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Salary', font=('Arial Black', 12))
            ],
            'employees': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Name', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Passport Number', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Passport Issued', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Passport Date', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Address', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Phone Number', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Position', font=('Arial Black', 12))
            ],
            'time_intervals': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Start time', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Duration', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='End time', font=('Arial Black', 12))
            ],
            'bookings': [
                CTkLabel(self.__update_entries_frame, text='ID', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Client', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Price', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Room', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Room type', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Time interval', font=('Arial Black', 12)),
                CTkLabel(self.__update_entries_frame, text='Employee', font=('Arial Black', 12))
            ]
        }
        self.__old_id: str = ''
        self.__radio_var: IntVar = IntVar()
        self.__old_radio_var: IntVar = IntVar()
        self.__list_of_radio: list = [
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Bookings',
                variable=self.__radio_var,
                value=0,
                command=self.__choose_table_click
            ),
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Client statuses',
                variable=self.__radio_var,
                value=1,
                command=self.__choose_table_click
            ),
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Clients',
                variable=self.__radio_var,
                value=2,
                command=self.__choose_table_click
            ),
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Employees',
                variable=self.__radio_var,
                value=3,
                command=self.__choose_table_click
            ),
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Positions',
                variable=self.__radio_var,
                value=4,
                command=self.__choose_table_click
            ),
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Room types',
                variable=self.__radio_var,
                value=5,
                command=self.__choose_table_click
            ),
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Rooms',
                variable=self.__radio_var,
                value=6,
                command=self.__choose_table_click
            ),
            CTkRadioButton(
                self.__radio_buttons_frame,
                text='Time intervals',
                variable=self.__radio_var,
                value=7,
                command=self.__choose_table_click
            )
        ]
        self.__dict_of_tables: dict = {
            '0': 'bookings',
            '1': 'client_status',
            '2': 'clients',
            '3': 'employees',
            '4': 'positions',
            '5': 'room_types',
            '6': 'rooms',
            '7': 'time_intervals'
        }
        self.__columns: dict = {
            'bookings': ('id', 'clients_id', 'price', 'room_id', 'room_types_id', 'time_intervals_id', 'employees_id'),
            'client_status': ('id', 'title', 'discount'),
            'clients': ('id', 'name', 'tNumber', 'email', 'client_status_id'),
            'employees': ('id', 'name', 'passport_number', 'passport_issued', 'passport_date', 'address', 'tNumber',
                          'positions_id'),
            'positions': ('id', 'titile', 'salary'),
            'room_types': ('id', 'title', 'cost_per_hour'),
            'rooms': ('id', 'room_types_id', 'number', 'status'),
            'time_intervals': ('id', 'start_time', 'duration', 'end_time')
        }
        self.__columns_output_names = {
            'bookings': ('ID', 'Client', 'Price', 'Room', 'Room type', 'Time interval', 'Employee'),
            'client_status': ('ID', 'Title', 'Discount'),
            'clients': ('ID', 'Name', 'Phone number', 'Email', 'Client status'),
            'employees': ('ID', 'Name', 'Passport number', 'Passport issued', 'Passport date', 'Address',
                          'Phone number', 'Position'),
            'positions': ('ID', 'Title', 'Salary'),
            'room_types': ('ID', 'Title', 'Cost/hour'),
            'rooms': ('ID', 'Room type', 'Number', 'Status'),
            'time_intervals': ('ID', 'Start time', 'Duration', 'End time')
        }
        self.__input_values: dict = {'names': [], 'values': []}
        self.__input_values_mul: dict = {}

        # ------------------Упаковка в окно-------------------

        self.__grid_window()

    def __grid_window(self):
        print('Griding')

        # --------------------Quit Frame---------------------

        self.__quit_button.pack()
        self.__quit_frame.grid(column=2, row=0, rowspan=3)

        # --------------------Radio Frame--------------------

        for i in self.__list_of_radio:
            i.pack(side='top', padx=5, pady=2, anchor='w')
        self.__radio_buttons_frame.grid(column=0, row=0)

        # --------------------Table Frame--------------------

        self.__table.pack(fill='both')
        self.__table.bind('<ButtonRelease-1>', self.__select_table_item)
        self.__table_frame.grid(column=1, row=0)

        # ----------------Update Buttons Frame---------------

        self.__delete_button.pack(side='left', padx=10)
        self.__update_button.pack(side='right', padx=10)
        self.__add_button.pack(side='right', padx=10)
        self.__update_buttons_frame.grid(column=1, row=2)

        # ----------------Update Entries Frame---------------

        self.__input_label.grid(column=0, row=1)
        self.__update_entries_frame.grid(column=1, row=1)

    def __set_table(self, columns_output: tuple, values: list):
        print('Setting table')

        # удаление старых полей таблицы и самой таблицы
        self.__table.delete(*self.__table.get_children())
        self.__table.configure(columns=columns_output, show='headings', selectmode='extended')

        # упаковка новых столбцов
        for i in columns_output:
            self.__table.heading(column=i, text=i)
            self.__table.column(i, minwidth=0, width=len(i) * 20, stretch=False)
            self.__input_values['names'].append(i)

        # обновление внешних значений
        self.__update_combo_values()
        self.__update_combo_boxes_values()

        # вставка значений в таблицу
        for value in values:
            self.__table.insert("", 'end', values=value)

    def __choose_table_click(self):
        print('Table chose')

        # выбор таблицы, удаление старой и подготовка для вставки новой

        # удаление старых данных (затирание)
        self.__forget_grid_values_entries_labels()
        self.__input_values['values'] = []
        self.__column_types = {}
        self.__input_values['names'] = []
        table = self.__dict_of_tables[str(self.__radio_var.get())]

        # получение данных новой таблицы
        res_columns = self.__db.get_columns(table)
        res_values = self.__db.get_values(table)
        index: int = 0
        self.__columns[table] = res_columns['columns']

        # вставка типов значений (не знаю зачем)
        for i in res_columns['types']:
            self.__column_types[res_columns['columns'][index]] = i
            index += 1

        # вставка новой таблицы
        self.__set_table(values=res_values, columns_output=self.__columns_output_names[table])

        # упаковка новых полей для ввода и лейблов
        index = 0
        for i in self.__dict_of_entries[table]:
            i.grid(column=index + 1, row=1, padx=5, pady=2)
            index += 1

        index = 0
        for i in self.__dict_of_labels[table]:
            i.grid(column=index + 1, row=0, padx=5, pady=2, sticky='w')
            index += 1

        self.__old_radio_var.set(self.__radio_var.get())

    def __select_table_item(self, _):
        print('Row selected')
        self.__input_values['values'] = []
        cur_item = self.__table.focus()
        values_item = self.__table.item(cur_item)['values']
        table: str = self.__dict_of_tables[str(self.__radio_var.get())]
        index: int = 0

        # заполнение полей для ввода
        for i in values_item:
            if type(self.__dict_of_entries[table][index]) is CTkEntry:
                self.__dict_of_entries[table][index].delete(0, 'end')
                self.__dict_of_entries[table][index].insert('end', i)
                if index == 0:
                    self.__old_id = self.__dict_of_entries[table][index].get()
            else:
                self.__dict_of_entries[table][index].set(i)
            self.__input_values['values'].append(i)
            index += 1

    def __update_combo_values(self):
        print('Getting combo vars')

        # инициализация словарей и отдельных списков (иначе будет сложнее с этим работать)
        self.__combo_values['rooms'] = {
            'ids': [],
            'names': []
        }
        self.__combo_values['clients'] = {
            'ids': [],
            'names': []
        }
        self.__combo_values['employees'] = {
            'ids': [],
            'names': []
        }
        self.__combo_values['bookings'] = {
            'clients': {
                'ids': [],
                'names': []
            },
            'rooms': {
                'ids': [],
                'names': []
            },
            'time_intervals': {
                'ids': [],
                'names': []
            },
            'employees': {
                'ids': [],
                'names': []
            }
        }

        # заполнение внешних значений для таблицы с комнатами
        for i in self.__db.get_values('room_types'):
            self.__combo_values['rooms']['ids'].append(str(i[0]))
            self.__combo_values['rooms']['names'].append(str(i[1]))

        # заполнение внешних значений для таблицы клиентов
        for i in self.__db.get_values('client_status'):
            self.__combo_values['clients']['ids'].append(str(i[0]))
            self.__combo_values['clients']['names'].append(str(i[1]))

        # заполнение внешних значений для таблицы работников
        for i in self.__db.get_values('positions'):
            self.__combo_values['employees']['ids'].append(str(i[0]))
            self.__combo_values['employees']['names'].append(str(i[1]))

        # заполнение внешних элементов таблицы клиентов для таблицы заявок
        for i in self.__db.get_values('clients'):
            self.__combo_values['bookings']['clients']['ids'].append(str(i[0]))
            self.__combo_values['bookings']['clients']['names'].append(str(i[1]))

        # заполнение внешних элементов таблицы комнат для таблицы заявок
        for i in self.__db.get_values('rooms'):
            self.__combo_values['bookings']['rooms']['ids'].append(str(i[0]))
            self.__combo_values['bookings']['rooms']['names'].append(str(i[2]))

        # заполнение внешних элементов таблицы интервалов времени для таблицы заявок
        for i in self.__db.get_values('time_intervals'):
            self.__combo_values['bookings']['time_intervals']['ids'].append(str(i[0]))
            self.__combo_values['bookings']['time_intervals']['names'].append(str(i[2]))

        # заполнение внешних элементов таблицы работников для таблицы заявок
        for i in self.__db.get_values('employees'):
            self.__combo_values['bookings']['employees']['ids'].append(str(i[0]))
            self.__combo_values['bookings']['employees']['names'].append(str(i[1]))

    def __update_combo_boxes_values(self):

        # здесь идёт обновление отдельных полей выбора для выбора внешних значений (кроме поля в bookings с room_types)
        self.__dict_of_entries['rooms'][1].configure(
            values=self.__combo_values['rooms']['names']
        )
        self.__dict_of_entries['clients'][4].configure(
            values=self.__combo_values['clients']['names']
        )
        self.__dict_of_entries['employees'][7].configure(
            values=self.__combo_values['employees']['names']
        )
        self.__dict_of_entries['bookings'][1].configure(
            values=self.__combo_values['bookings']['clients']['names']
        )
        self.__dict_of_entries['bookings'][3].configure(
            values=self.__combo_values['bookings']['rooms']['names']
        )
        self.__dict_of_entries['bookings'][5].configure(
            values=self.__combo_values['bookings']['time_intervals']['names']
        )
        self.__dict_of_entries['bookings'][6].configure(
            values=self.__combo_values['bookings']['employees']['names']
        )

    def __get_values(self, table: str) -> tuple:
        print('Getting values')
        values: tuple = ()
        for i in self.__dict_of_entries[table]:

            # получение введённого значения
            if type(i) == CTkEntry:
                values += (i.get(),)

            # получение выбранного значения
            if type(i) == CTkComboBox:

                # получение выбранного значения для таблиц rooms и bookings
                if table == 'rooms' or (table == 'bookings' and len(values) == 4):
                    name_id = [
                        n for n, x in enumerate(
                            self.__combo_values['rooms']['names']
                        ) if x == i.get()
                    ]
                    if name_id:
                        name_id = self.__combo_values['rooms']['ids'][name_id.pop(0)]
                    else:
                        raise ValueError('Значение не опознано')
                    values += (str(name_id),)

                # получение выбранного значения для таблиц clients
                elif table == 'clients':
                    name_id = [
                        n for n, x in enumerate(self.__combo_values['clients']['names']) if x == i.get()
                    ]
                    if name_id:
                        name_id = self.__combo_values['clients']['ids'][name_id.pop(0)]
                    else:
                        raise ValueError('Значение не опознано')
                    values += (str(name_id),)

                # по аналогии
                elif table == 'employees':
                    name_id = [
                        n for n, x in enumerate(self.__combo_values['employees']['names']) if x == i.get()
                    ]
                    if name_id:
                        name_id = self.__combo_values['employees']['ids'][name_id.pop(0)]
                    else:
                        raise ValueError('Значение не опознано')
                    values += (str(name_id),)

                # по аналогии, но обширнее
                elif table == 'bookings':

                    # получение id для внешнего значения из таблицы clients
                    if len(values) == 1:
                        name_id = [
                            n for n, x in enumerate(
                                self.__combo_values['bookings']['clients']['names']
                            ) if x == i.get()
                        ]
                        if name_id:
                            name_id = self.__combo_values['bookings']['clients']['ids'][name_id.pop(0)]
                        else:
                            raise ValueError('Значение не опознано')
                        values += (str(name_id),)

                    # получение id для внешнего значения из таблицы rooms
                    elif len(values) == 3:
                        room_id = [
                            n for n, x in enumerate(
                                self.__combo_values['bookings']['rooms']['names']
                            ) if x == i.get()
                        ]
                        if room_id:
                            room_id = self.__combo_values['bookings']['rooms']['ids'][room_id.pop(0)]
                        else:
                            raise ValueError('Значение не опознано')
                        values += (str(room_id),)

                    # по аналогии
                    elif len(values) == 5:
                        name_id = [
                            n for n, x in enumerate(
                                self.__combo_values['bookings']['time_intervals']['names']
                            ) if x == i.get()
                        ]
                        if name_id:
                            name_id = self.__combo_values['bookings']['time_intervals']['ids'][name_id.pop(0)]
                        else:
                            raise ValueError('Значение не опознано')
                        values += (str(name_id),)

                    # по аналогии
                    elif len(values) == 6:
                        name_id = [
                            n for n, x in enumerate(
                                self.__combo_values['bookings']['employees']['names']
                            ) if str(x) == str(i.get())
                        ]
                        if name_id:
                            name_id = self.__combo_values['bookings']['employees']['ids'][name_id.pop(0)]
                        else:
                            raise ValueError('Значение ' + str(i.get()) + ' не опознано')
                        values += (str(name_id),)
        return values

    def __insert_click(self):
        print('Inserting values')
        table = self.__dict_of_tables[str(self.__radio_var.get())]
        values: tuple = self.__get_values(table)

        # попытка вставки записи
        try:
            self.__db.input_value(
                table=table,
                columns=tuple(self.__columns[table][1:]),
                values=values[1:]
            )
            res_values = self.__db.get_values(self.__dict_of_tables[str(self.__radio_var.get())])
            self.__set_table(values=res_values, columns_output=self.__columns_output_names[table])
        except DatabaseError as e:
            mb.showerror('DatabaseError', 'Something went wrong...\n' + str(e.args))

    def __delete_click(self):
        print('Deleting values')
        table = self.__dict_of_tables[str(self.__radio_var.get())]

        # попытка удаления записи
        try:
            self.__db.delete_value(
                table=table,
                row_id=self.__old_id
            )
            res_values = self.__db.get_values(table)
            self.__set_table(values=res_values, columns_output=self.__columns_output_names[table])
        except DatabaseError as e:
            mb.showerror('DatabaseError', 'Something went wrong...\n' + str(e.args))

    def __update_click(self):
        print('Updating values')
        table = self.__dict_of_tables[str(self.__radio_var.get())]
        values: tuple = self.__get_values(table)

        # попытка вноса изменений
        try:
            self.__db.update_value(
                table=table,
                columns=tuple(self.__columns[table][1:]),
                values=values[1:],
                old_id=self.__old_id
            )
            res_values = self.__db.get_values(self.__dict_of_tables[str(self.__radio_var.get())])
            self.__set_table(values=res_values, columns_output=self.__columns_output_names[table])
        except DatabaseError as e:
            mb.showerror('DatabaseError', 'Something went wrong...\n' + str(e.args))

    def __validate_booking_room_types_combobox(self, choice):
        room_table_rows = self.__db.get_values('rooms')
        room_type: str = ''

        # поиск того самого значения для типа комнаты
        for i in room_table_rows:
            if str(i[2]) == str(choice):
                room_type = str(i[1])
        self.__dict_of_entries['bookings'][4].set(room_type)

    def __forget_grid_values_entries_labels(self):
        print('Forgetting grid of entries and labels')
        table = self.__dict_of_tables[str(self.__old_radio_var.get())]

        # удаление элементов старой таблицы с формы
        for i in self.__dict_of_entries[table]:
            if type(i) is CTkEntry:
                i.delete(0, 'end')
            else:
                i.set('')
            i.grid_forget()
        for i in self.__dict_of_labels[table]:
            i.grid_forget()

    def __quit_click(self):
        print('Quitting')

        # вывод окошка с вопросом
        question = mb.askokcancel('Quit', 'Are you sure?')
        if question:
            self.destroy()
