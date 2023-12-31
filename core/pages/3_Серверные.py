import hashlib

import streamlit as st
from pandas import DataFrame

from DAO.admin import AdminDAO
from DAO.server import ServerDAO
from main import servers, salt

st.set_page_config(
    page_title="Серверные",
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

    st.header('Список серверов')
    table: DataFrame = DataFrame([(
        server.server_num,
        server.server_name,
    ) for server in servers],
        columns=[
            "Номер серверной",
            "Имя серверной"
        ])

    st.dataframe(
        table,
        use_container_width=True,  # параметр для растяжения по всей ширине контейнера
        hide_index=True,
    )

    st.header('Добавить')
    with st.form(key='create_form'):
        st.write("Добавьте данные по серверным")
        server_num = st.text_input("Номер серверной")
        server_name = st.text_input("Имя серверной")
        created = st.form_submit_button("Добавить депарсервернуютамент")
        if created:
            try:
                ServerDAO().add({
                    'server_num': server_num,
                    'server_name': server_name
                })
                st.success(
                    'Серверная добавлена',
                )
            except Exception as e:
                st.error(f'Ошибка добавления: {e}')

    st.header('Обновить')
    select_server: str = st.selectbox(
        'Выберите серверную',
        options=[server.server_name for server in servers],
        key='select_server',
    )

    with st.form(key='edit_form'):
        edit_server_name: str = st.text_input(
            'Название',
            key='edit_serv_name',
            value=st.session_state.select_server if st.session_state.select_server else None
        )

        data: dict = {
            'server_name': st.session_state.edit_serv_name,
        }
        updated = st.form_submit_button("Обновить сервер")
        if updated:
            try:
                ServerDAO().update(
                    id_x=[
                        server.server_num for server in servers
                        if server.server_name == st.session_state.select_server
                    ][0],
                    data=data
                )
                st.success(
                    'Сервер обновлен',
                )
            except Exception as e:
                st.error(f'Ошибка обновления: {e}')

    st.header('Удалить')
    with st.form(key='delete_form'):
        select_server: str = st.selectbox(
            'Выберите сотрудника',
            options=[server.server_name for server in servers],
            key='delete_server',
        )
        deleted = st.form_submit_button("Удалить сервер")
        if deleted:
            try:
                ServerDAO().delete(
                    id_x=[
                        server.server_num for server in servers
                        if server.server_name == st.session_state.delete_server
                    ][0]
                )
                st.success(
                    'Сервер удален',
                )
            except Exception as e:
                st.error(f'Ошибка удаления: {e}')
else:
    st.warning(
        'Введен неверный логин или пароль',
    )
