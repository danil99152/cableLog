import hashlib
import os

import streamlit as st
from pandas import DataFrame

from DAO.DB.engine import engine
from DAO.admin import AdminDAO
from DAO.aws import AwsDAO
from DAO.cable_line import CableLineDAO
from DAO.department import DepartmentDAO
from DAO.employee import EmployeeDAO
from DAO.models import Base, CableLine, Employee, AWS, Department, Server
from DAO.server import ServerDAO

from dotenv import load_dotenv

# Содержимое страницы во весь экран
st.set_page_config(
    layout='wide'
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

load_dotenv()

salt = b'salt'  # Получение соли, сохраненной для этого пользователя

# Проверка существования админа
if not AdminDAO().get(1):
    password = os.getenv('PASSWORD')
    encoded_password = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    AdminDAO.add({
        'login': os.getenv('LOGIN'),
        'password': encoded_password,
    })

# Списки объектов всех таблиц из БД
cable_lines: list[CableLine] = CableLineDAO().get_all()
employees: list[Employee] = EmployeeDAO().get_all()
aws: list[AWS] = AwsDAO().get_all()
departments: list[Department] = DepartmentDAO().get_all()
servers: list[Server] = ServerDAO().get_all()

# Скрытые таблицы
with st.expander('Подразделения'):
    table: DataFrame = DataFrame([(
        department.department_name,
    ) for department in departments],
        columns=[
            "Подразделение"
        ])

    st.dataframe(
        table
    )

with st.expander('Работники'):
    table: DataFrame = DataFrame([(
        employee.full_name,
        employee.department.department_name,
    ) for employee in employees],
        columns=[
            "ФИО",
            "Подразделение"
        ])
    st.dataframe(
        table
    )

with st.expander('Серверные'):
    table: DataFrame = DataFrame([(
        server.server_num,
        server.server_name,
    ) for server in servers],
        columns=[
            "Номер серверной",
            "Имя серверной"
        ])

    st.dataframe(
        table
    )

with st.expander("Список АРМ"):
    table: DataFrame = DataFrame([(
        aw.pc_name,
        aw.ip,
        aw.mac,
        aw.employee.full_name
    ) for aw in aws],
        columns=[
            "Имя АРМ",
            "IP адрес АРМ",
            "MAC адрес АРМ",
            "Работник АРМ",
        ])

    st.dataframe(
        table
    )

st.divider()

# Генерация таблицы при помощи DataFrame от pandas и функции table от Streamlit
st.write("Список кабельных линий")
cable_lines_table: DataFrame = DataFrame([(
    cable_line.socket_num,
    cable_line.socket_port,
    cable_line.patchpanel_port,
    cable_line.length,
    cable_line.aws.employee.full_name,
    cable_line.aws.employee.department.department_name,
    cable_line.aws.pc_name,
    cable_line.aws.ip,
    cable_line.aws.mac,
    cable_line.server.server_name
) for cable_line in cable_lines],
    columns=[
        "№ розетки",
        "№ порта розетки",
        "№ порта на патчпанели",
        "Длина",
        "ФИО",
        "Подразделение",
        "Имя АРМ",
        "IP адрес АРМ",
        "MAC адрес АРМ",
        "Серверная"
    ])

st.dataframe(
    cable_lines_table,
    use_container_width=True,  # параметр для растяжения по всей ширине контейнера
    column_config={
        '№ розетки': st.column_config.NumberColumn(
            format="№ %d",
        ),
        '№ порта розетки': st.column_config.NumberColumn(
            format="№ %d",
        ),
        '№ порта на патчпанели': st.column_config.NumberColumn(
            format="№ %d",
        ),
        'Длина': st.column_config.NumberColumn(
            format="%dм",
        ),
    },
)
