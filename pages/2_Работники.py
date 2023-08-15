import streamlit as st
from pandas import DataFrame

from DAO.admin import AdminDAO
from DAO.employee import EmployeeDAO
from main import departments, employees, salt
import hashlib


st.set_page_config(
    page_title="Рабочие",
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

    # Список сотрудников
    st.header('Список сотрудников')
    table: DataFrame = DataFrame([(
        employee.id,
        employee.surname,
        employee.name,
        employee.middlename,
        employee.department.department_name,
    ) for employee in employees],
        columns=[
            "id",
            "Фамилия",
            "Имя",
            "Отчество",
            "Подразделение",
        ])

    st.dataframe(
        table,
        use_container_width=True,  # параметр для растяжения по всей ширине контейнера
        hide_index=True,
    )

    # Добавить сотрудника
    st.header('Добавить')
    with st.form(key='create_form'):
        st.write("Введите данные сотрудника")
        surname = st.text_input("Фамилия")
        name = st.text_input("Имя")
        middlename = st.text_input("Отчество")

        created = st.form_submit_button("Добавить работника")
        if created:
            try:
                EmployeeDAO().add({
                    'surname': surname,
                    'name': name,
                    'middlename': middlename,
                    'department_id': [
                        department.id for department in departments
                        if department.department_name == st.session_state.add_employee
                    ][0]
                })
                st.success(
                    'Работник добавлен',
                )
            except Exception as e:
                st.error(f'Ошибка добавления: {e}')

    # Обновить сотрудника
    st.header('Обновить')
    select_employee: str = st.selectbox(
        'Выберите сотрудника',
        options=[employee.full_name for employee in employees],
        key='select_employee',
    )
    with st.form(key='edit_form'):
        edit_surname: str = st.text_input(
            'Фамилия',
            key='edit_surname',
            value=st.session_state.select_employee.split()[0] if st.session_state.select_employee else None
        )
        edit_name: str = st.text_input(
            'Имя',
            key='edit_name',
            value=st.session_state.select_employee.split()[1] if st.session_state.select_employee else None
        )
        edit_middlename: str = st.text_input(
            'Отчество',
            key='edit_middlename',
            value=st.session_state.select_employee.split()[2] if st.session_state.select_employee else None
        )
        edit_department = st.selectbox(
            'Подразделение',
            options=[department.department_name for department in departments],
            key='edit_department'
        )

        data: dict = {
            'surname': st.session_state.edit_surname,
            'name': st.session_state.edit_name,
            'middlename': st.session_state.edit_middlename,
            'department_id': [
                department.id for department in departments
                if department.department_name == st.session_state.edit_department
            ][0]}

        updated = st.form_submit_button("Обновить работника")
        if updated:
            try:
                EmployeeDAO().update(
                    id_x=[
                        employee.id for employee in employees
                        if employee.full_name == st.session_state.select_employee
                    ][0],
                    data=data
                )
                st.success(
                    'Работник обновлен',
                )
            except Exception as e:
                st.error(f'Ошибка обновления: {e}')

    # Удаление сотрудника
    st.header('Удалить')
    with st.form(key='delete_form'):
        select_employee: str = st.selectbox(
            'Выберите сотрудника',
            options=[employee.full_name for employee in employees],
            key='delete_employee',
        )
        deleted = st.form_submit_button("Удалить работника")
        if deleted:
            try:
                EmployeeDAO().delete(
                    id_x=[
                        employee.id for employee in employees
                        if employee.full_name == st.session_state.delete_employee
                    ][0]
                )
                st.success(
                    'Работник удален',
                )
            except Exception as e:
                st.error(f'Ошибка удаления: {e}')
else:
    st.warning(
        'Введен неверный логин или пароль',
    )
