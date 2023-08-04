import random
import sqlite3
import string

import pandas as pd
import streamlit as st

# Подключение к БД
conn = sqlite3.connect('cables.db')
c = conn.cursor()

# Создание таблиц
c.execute('''
          CREATE TABLE IF NOT EXISTS servers
          (server_num INTEGER PRIMARY KEY,
           server_name TEXT UNIQUE)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS departments
          (id INTEGER PRIMARY KEY,
           department_name TEXT UNIQUE)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS employees 
          (id INTEGER PRIMARY KEY, 
           surname TEXT,
           name TEXT,
           middlename TEXT,
           department_id INTEGER REFERENCES department(id))
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS aws
          (id INTEGER PRIMARY KEY,
           socket_num INT UNIQUE,  
           socket_port INT UNIQUE,
           patchpanel_port INT UNIQUE,
           length INT, 
           pc_name TEXT UNIQUE,
           ip TEXT UNIQUE,  
           mac TEXT UNIQUE,
           server_num INTEGER REFERENCES server(server_num),
           employee_id INTEGER REFERENCES employees(id))
          ''')


# Функции записи данных
def add_server(server_num, server_name):
    c.execute("INSERT INTO servers VALUES (?, ?)", (server_num, server_name))
    conn.commit()


def add_department(department_name):
    c.execute("INSERT INTO departments VALUES (?, ?)", (None, department_name))
    conn.commit()


def add_aw(socket_num, socket_port, patchpanel_port, length, pc_name, ip, mac, server_num, employee):
    c.execute("INSERT INTO aws VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (socket_num, socket_port, patchpanel_port, length, pc_name, ip, mac, server_num, employee))
    conn.commit()


def add_employee(surname, name, middlename, department_id):
    c.execute("INSERT INTO employees VALUES (NULL, ?, ?, ?, ?)",
              (surname, name, middlename, department_id))
    conn.commit()


# Формы ввода данных
st.write("Добавьте департаменты")
department_name = st.text_input("Имя департамента")
if st.button("Добавить департамент"):
    add_department(department_name)

st.write("Введите данные сотрудника")
surname = st.text_input("Фамилия")
name = st.text_input("Имя")
middlename = st.text_input("Отчество")

c.execute("SELECT id, department_name FROM departments")
departments = dict((x, y) for x, y in c.fetchall())
department = st.selectbox('Выберите департамент',
                          options=list(departments.keys()),
                          format_func=lambda x: departments[x])

if st.button("Добавить работника"):
    add_employee(surname, name, middlename, department)

st.write("Добавьте данные по серверным")
server_num = st.text_input("Номер серверной")
server_name = st.text_input("Имя серверной")
if st.button("Добавить серверную"):
    add_server(server_num, server_name)

st.write("Введите данные АРМ")
socket_num = st.text_input("Номер розетки")
socket_port = st.text_input("Номер порта розетки")
patchpanel_port = st.text_input("Номер порта на патчпанели")
length = st.text_input("Длина")
pc_name = st.text_input("Имя АРМ")
ip = st.text_input("IP адрес АРМ")
mac = st.text_input("MAC адрес АРМ")

c.execute("SELECT id, surname || ' ' || name || ' ' || middlename FROM employees")
employees = dict((x, y) for x, y in c.fetchall())
employee = st.selectbox('Выберите сотрудника',
                        options=list(employees.keys()),
                        format_func=lambda x: employees[x])

c.execute("SELECT server_num, server_name FROM servers")
servers = dict((x, y) for x, y in c.fetchall())
server_num = st.selectbox('Выберите серверную',
                          options=list(servers.keys()),
                          format_func=lambda x: servers[x])

if st.button("Добавить АРМ"):
    add_aw(socket_num, socket_port, patchpanel_port, length, pc_name, ip, mac, server_num, employee)


# Кнопка случайной генерации трех записей
def random_string(l: int = 8) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(l))


def generate_random_data():
    for i in range(3):
        department_name = random_string(10)
        add_department(department_name)

        surname = random_string(20)
        name = random_string(20)
        middlename = random_string(20)
        c.execute("SELECT id FROM departments ORDER BY id DESC LIMIT 1")
        department_id = c.fetchone()[0]
        add_employee(surname, name, middlename, department_id)

        c.execute("SELECT server_num FROM servers ORDER BY server_num DESC LIMIT 1")
        server_num = c.fetchone()
        server_num = 1 if not server_num else server_num[0] + 1
        server_name = random_string(10) + str(server_num)
        add_server(server_num, server_name)

        socket_num = random.randint(1, 10000)
        socket_port = random.randint(1, 10000)
        patchpanel_port = random.randint(1, 10000)
        length = random.randint(10, 1000)
        pc_name = random_string(14)
        ip = random_string(14)
        mac = random_string(14)
        c.execute("SELECT server_num FROM servers ORDER BY server_num DESC LIMIT 1")
        server_num = c.fetchone()[0]
        c.execute("SELECT id FROM employees ORDER BY id DESC LIMIT 1")
        employee = c.fetchone()[0]
        add_aw(socket_num, socket_port, patchpanel_port, length, pc_name, ip, mac, server_num, employee)


if st.button("Сгенерировать случайно 3 записи"):
    generate_random_data()

# Запрос на объединение двух таблиц
query = """
SELECT a.socket_num, a.socket_port, a.patchpanel_port, 
a.length, e.surname || ' ' || e.name || ' ' || e.middlename, d.department_name, a.pc_name, a.ip, a.mac,
s.server_name 
FROM aws as a
INNER JOIN servers as s ON a.server_num = s.server_num
INNER JOIN employees as e ON e.id = a.employee_id
INNER JOIN departments as d ON e.department_id = d.id
"""

c.execute(query)
data = c.fetchall()

# Генерация таблицы при помощи DataFrame от pandas и функции table от Streamlit
df = pd.DataFrame(
    data=data,
    columns=[
        "№ розетки", "№ порта розетки", "№ порта на патчпанели",
        "Длина", "ФИО", "Подразделение", "Имя АРМ", "IP адрес АРМ", "MAC адрес АРМ",
        "Серверная"
    ])

st.table(data=df)
