import hashlib

import streamlit as st
from pandas import DataFrame

from DAO.admin import AdminDAO
from DAO.aws import AwsDAO
from main import aws, employees, salt

st.set_page_config(
    page_title="АРМы",
    layout='wide'
)

login: str = st.text_input(
    'Логин',
)
password: str = st.text_input(
    'Пароль',
    type='password'
)

db_login = AdminDAO().get(index=1)[0].login
key = AdminDAO().get(index=1)[0].password

encoded_password = hashlib.pbkdf2_hmac(
    'sha256',
    password.encode('utf-8'),
    salt,
    100000
)

if login == db_login and encoded_password == key:

    st.header('Список АРМов')
    table: DataFrame = DataFrame([(
        aw.id,
        aw.pc_name,
        aw.ip,
        aw.mac,
        aw.employee.full_name,
    ) for aw in aws],
        columns=[
            "id",
            "Имя АРМ",
            "IP адрес АРМ",
            "MAC адрес АРМ",
            "Работник АРМ",
        ])

    st.dataframe(
        table,
        use_container_width=True,  # параметр для растяжения по всей ширине контейнера
        hide_index=True,
    )

    st.header('Добавить')
    with st.form(key='create_form'):
        st.write("Введите данные АРМ")
        pc_name = st.text_input("Имя АРМ")
        ip = st.text_input("IP адрес АРМ")
        mac = st.text_input("MAC адрес АРМ")

        employee = st.selectbox(
            'Выберите сотрудника',
            options=[employee.full_name for employee in employees],
            key='add_aws',
        )

        created = st.form_submit_button("Добавить АРМ")
        if created:
            try:
                AwsDAO().add({
                    'pc_name': pc_name,
                    'ip': ip,
                    'mac': mac,
                    'employee_id': [
                        employee.id for employee in employees
                        if employee.full_name == st.session_state.add_aws
                    ][0]
                })
                st.success(
                    'АРМ добавлен',
                )
            except Exception as e:
                st.error(f'Ошибка добавления: {e}')

    aws_dict = dict(((
                         aw.ip,
                         aw.mac,
                         aw.employee_id
                     ),
                     aw.pc_name) for aw in aws)
    st.header('Обновить')
    select_aws: str = st.selectbox(
        'Выберите АРМ',
        options=list(aws_dict.keys()),
        format_func=lambda x: aws_dict[x],
        key='select_aws',
    )

    with st.form(key='edit_form'):
        edit_pc_name: str = st.text_input(
            'Имя АРМ',
            key='edit_pc_name',
            value=aws_dict[st.session_state.select_aws] if st.session_state.select_aws else None
        )
        edit_ip: str = st.text_input(
            'IP адрес АРМ',
            key='edit_ip',
            value=st.session_state.select_aws[0] if st.session_state.select_aws else None
        )
        edit_mac: str = st.text_input(
            'MAC адрес АРМ',
            key='edit_mac',
            value=st.session_state.select_aws[1] if st.session_state.select_aws else None
        )
        edit_employee = st.selectbox(
            'Работник',
            options=[employee.full_name for employee in employees],
            index=st.session_state.select_aws[2] - 1,
            key='edit_employee'
        )

        data: dict = {
            'pc_name': st.session_state.edit_pc_name,
            'ip': st.session_state.edit_ip,
            'mac': st.session_state.edit_mac,
            'employee_id': [
                employee.id for employee in employees
                if employee.full_name == st.session_state.edit_employee
            ][0]}

        updated = st.form_submit_button("Обновить АРМ")
        if updated:
            try:
                AwsDAO().update(
                    id_x=[
                        aw.id for aw in aws
                        if aw.pc_name == st.session_state.select_aw
                    ][0],
                    data=data
                )
                st.success(
                    'АРМ обновлен',
                )
            except Exception as e:
                st.error(f'Ошибка обновления: {e}')

    st.header('Удалить')
    with st.form(key='delete_form'):
        select_aws: str = st.selectbox(
            'Выберите АРМ',
            options=[aw.pc_name for aw in aws],
            key='delete_aws',
        )
        deleted = st.form_submit_button("Удалить АРМ")
        if deleted:
            try:
                AwsDAO().delete(
                    id_x=[
                        aw.id for aw in aws
                        if aw.pc_name == st.session_state.delete_aws
                    ][0]
                )
                st.success(
                    'АРМ удален',
                )
            except Exception as e:
                st.error(f'Ошибка удаления: {e}')

else:
    st.warning(
        'Введен неверный логин или пароль',
    )
