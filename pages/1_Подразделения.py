import hashlib

import streamlit as st
from pandas import DataFrame

from DAO.admin import AdminDAO
from DAO.department import DepartmentDAO
from DAO.models import Department
from main import departments, salt

st.set_page_config(
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

    st.header('Список департаментов')
    table: DataFrame = DataFrame([(
        department.id,
        department.department_name,
    ) for department in departments],
        columns=[
            "id",
            "Подразделение"
        ])

    st.dataframe(
        table,
        use_container_width=True,  # параметр для растяжения по всей ширине контейнера
        hide_index=True,
    )

    st.header('Добавить')
    with st.form(key='create_form'):
        st.header("Добавьте департаменты")
        department_name = st.text_input("Имя департамента")
        created = st.form_submit_button("Добавить департамент")
        if created:
            try:
                DepartmentDAO().add({
                    'department_name': department_name
                })
                st.success(
                    'Департамент добавлен',
                )
            except Exception as e:
                st.error(f'Ошибка добавления: {e}')

    st.header('Обновить')
    select_department: list[Department] = st.selectbox(
        'Выберите департамент',
        options=[department.department_name for department in departments],
        key='select_department',
    )
    with st.form(key='edit_form'):
        edit_department_name: str = st.text_input(
            'Название',
            key='edit_dep_name',
            value=st.session_state.select_department.split()[0] if st.session_state.select_department else None
        )

        data: dict = {
            'department_name': st.session_state.edit_dep_name,
        }
        updated = st.form_submit_button("Обновить департамент")
        if updated:
            try:
                DepartmentDAO().update(
                    id_x=[
                        department.id for department in departments
                        if department.department_name == st.session_state.select_department
                    ][0],
                    data=data
                )
                st.success(
                    'Департамент обновлен',
                )
            except Exception as e:
                st.error(f'Ошибка обновления: {e}')

    st.header('Удалить')
    with st.form(key='delete_form'):
        select_department: list[Department] = st.selectbox(
            'Выберите сотрудника',
            options=[department.department_name for department in departments],
            key='delete_department',
        )
        deleted = st.form_submit_button("Удалить департамент")
        if deleted:
            try:
                DepartmentDAO().delete(
                    id_x=[
                        department.id for department in departments
                        if department.department_name == st.session_state.delete_department
                    ][0]
                )
                st.success(
                    'Департамент удален',
                )
            except Exception as e:
                st.error(f'Ошибка удаления: {e}')
else:
    st.warning(
        'Введен неверный логин или пароль',
    )
