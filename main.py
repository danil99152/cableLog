import streamlit as st
from pandas import DataFrame

from DAO.DB.engine import engine
from DAO.aws import AwsDAO
from DAO.cable_line import CableLineDAO
from DAO.department import DepartmentDAO
from DAO.employee import EmployeeDAO
from DAO.models import Base, CableLine, Employee, AWS, Department, Server
from DAO.server import ServerDAO

# Содержимое страницы во весь экран
st.set_page_config(
    layout='wide'
)

# Создание таблиц
Base.metadata.create_all(bind=engine)

# Списки объектов всех таблиц из БД
cable_lines: list[CableLine] = CableLineDAO().get_all()
employees: list[Employee] = EmployeeDAO().get_all()
aws: list[AWS] = AwsDAO().get_all()
departments: list[Department] = DepartmentDAO().get_all()
servers: list[Server] = ServerDAO().get_all()

# Формы ввода данных
st.write("Добавьте департаменты")
department_name = st.text_input("Имя департамента")
if st.button("Добавить департамент"):
    DepartmentDAO().add({
        'department_name': department_name
    })

st.write("Введите данные сотрудника")
surname = st.text_input("Фамилия")
name = st.text_input("Имя")
middlename = st.text_input("Отчество")

department = st.selectbox(
    'Выберите департамент',
    options=[department.department_name for department in departments],
    key='add_employee',
)

if st.button("Добавить работника"):
    EmployeeDAO().add({
        'surname': surname,
        'name': name,
        'middlename': middlename,
        'department_id': [
            department.id for department in departments
            if department.department_name == st.session_state.add_employee
        ][0]
    })

st.write("Добавьте данные по серверным")
server_num = st.text_input("Номер серверной")
server_name = st.text_input("Имя серверной")
if st.button("Добавить серверную"):
    ServerDAO().add({
        'server_num': server_num,
        'server_name': server_name
    })

st.write("Введите данные АРМ")
pc_name = st.text_input("Имя АРМ")
ip = st.text_input("IP адрес АРМ")
mac = st.text_input("MAC адрес АРМ")

employee = st.selectbox(
    'Выберите сотрудника',
    options=[employee.full_name for employee in employees],
    key='add_aws',
)

if st.button("Добавить АРМ"):
    AwsDAO().add({
        'pc_name': pc_name,
        'ip': ip,
        'mac': mac,
        'employee_id': [
            employee.id for employee in employees
            if employee.full_name == st.session_state.add_aws
        ][0]
    })

st.write("Введите данные кабельной линии")
socket_num = st.text_input("Номер розетки")
socket_port = st.text_input("Номер порта розетки")
patchpanel_port = st.text_input("Номер порта на патчпанели")
length = st.text_input("Длина")

add_aws = st.selectbox(
    'Выберите АРМ',
    options=[aw.pc_name for aw in aws],
    key='add_cl',
)

add_server_num = st.selectbox(
    'Выберите сервер',
    options=[server.server_name for server in servers],
    key='add_cl2',
)

if st.button("Добавить кабельную линию"):
    CableLineDAO().add({
        'socket_num': socket_num,
        'socket_port': socket_port,
        'patchpanel_port': patchpanel_port,
        'length': length,
        'aws_id': [
            aw.id for aw in aws
            if aw.pc_name == st.session_state.add_cl
        ][0],
        'server_id': [
            server.server_num for server in servers
            if server.server_name == st.session_state.add_cl2
        ][0]
    })

# Генерация таблицы при помощи DataFrame от pandas и функции table от Streamlit
table: DataFrame = DataFrame([(
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
    table,
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
