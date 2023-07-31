import sqlite3

import pandas as pd
import streamlit as st

# Подключение к БД
conn = sqlite3.connect('cables.db')
c = conn.cursor()

# Создание таблиц
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
           server_num INT)
          ''')

c.execute('''
          CREATE TABLE IF NOT EXISTS employees 
          (id INTEGER PRIMARY KEY, 
           name TEXT,
           department TEXT,
           aw_id INTEGER REFERENCES aws(id))
          ''')


# Функции записи данных
def add_aw(socket_num, socket_port, patchpanel_port, length, pc_name, ip, mac, server_num):
    c.execute("INSERT INTO aws VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?)",
              (socket_num, socket_port, patchpanel_port, length, pc_name, ip, mac, server_num))
    conn.commit()


def add_employee(name, department, aw_id):
    c.execute("INSERT INTO employees VALUES (NULL, ?, ?, ?)",
              (name, department, aw_id))
    conn.commit()


# Формы ввода данных
st.write("Введите данные АРМ")
socket_num = st.text_input("Номер розетки")
socket_port = st.text_input("Номер порта розетки")
patchpanel_port = st.text_input("Номер порта на патчпанели")
length = st.text_input("Длина")
pc_name = st.text_input("Имя АРМ")
ip = st.text_input("IP адрес АРМ")
mac = st.text_input("MAC адрес АРМ")
server_num = st.text_input("Номер серверной")

if st.button("Добавить АРМ"):
    add_aw(socket_num, socket_port, patchpanel_port, length, pc_name, ip, mac, server_num)

st.write("Введите данные сотрудника")
name = st.text_input("ФИО")
department = st.text_input("Подразделение")
aw_id = st.text_input("ID АРМ")

if st.button("Добавить работника"):
    add_employee(name, department, aw_id)

# Вывод данных из двух таблиц
# c.execute("SELECT * FROM aws")
# aws = c.fetchall()
#
# c.execute("SELECT * FROM employees")
# employees = c.fetchall()
#
# st.write(aws)
# st.write(employees)

# Запрос на объединение двух таблиц
query = """
SELECT e.name, e.department, 
a.socket_num, a.socket_port, a.patchpanel_port, a.length, a.pc_name, a.ip, a.mac 
FROM employees as e
JOIN aws as a ON e.aw_id = a.id
"""

c.execute(query)
data = c.fetchall()

# Генерация таблицы при помощи DataFrame от pandas и функции table от Streamlit
df = pd.DataFrame(
   data=data,
   columns=("№ розетки", "№ порта розетки", "№ порта на патчпанели",
            "Длина", "ФИО", "Подразделение", "Имя АРМ", "IP адрес АРМ",
            "MAC адрес АРМ"))

st.table(data=df)
