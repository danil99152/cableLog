import streamlit as st

from DAO.cable_line import CableLineDAO
from DAO.models import CableLine
from main import aws, servers, cable_lines_table, cable_lines

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

if login == "admin" and password == '1234':

    st.header('Список кабельных линий')
    st.dataframe(
        cable_lines_table,
        use_container_width=True,  # параметр для растяжения по всей ширине контейнера
        column_config={
            '№ розетки': st.column_config.NumberColumn(),
            '№ порта розетки': st.column_config.NumberColumn(),
            '№ порта на патчпанели': st.column_config.NumberColumn(),
            'Длина': st.column_config.NumberColumn(),
        },
    )

    st.header('Добавить')
    with st.form(key='create_form'):
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

        created = st.form_submit_button("Добавить кабельную линию")
        if created:
            try:
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
                st.success(
                    'Линия добавлена',
                )
            except Exception as e:
                st.error(f'Ошибка добавления: {e}')

    st.header('Обновить')
    select_cl: list[CableLine] = st.selectbox(
        'Выберите кабельную линию',
        options=[str(cl.id) for cl in cable_lines],
        key='select_cl',
    )
    with st.form(key='edit_form'):
        edit_socket: str = st.text_input(
            'Номер розетки',
            key='socket_num',
            value=st.session_state.select_cl.split()[0] if st.session_state.select_cl else None
        )
        edit_socket_port: str = st.text_input(
            'Номер порта розетки',
            key='socket_port',
            value=st.session_state.select_cl.split()[1] if st.session_state.select_cl else None
        )
        edit_patchpanel: str = st.text_input(
            'Номер порта патчпанели',
            key='patch_panel',
            value=st.session_state.select_cl.split()[2] if st.session_state.select_cl else None
        )
        edit_length: str = st.text_input(
            'Длина',
            key='length',
            value=st.session_state.select_cl.split()[3] if st.session_state.select_cl else None
        )
        edit_department = st.selectbox(
            'АРМ',
            options=[aw.pc_name for aw in aws],
            key='edit_aws'
        )
        edit_server = st.selectbox(
            'Серверная',
            options=[server.server_name for server in servers],
            key='edit_server'
        )

        data: dict = {
            'socket_num': st.session_state.edit_surname,
            'socket_port': st.session_state.edit_name,
            'patch_panel': st.session_state.edit_middlename,
            'length': st.session_state.edit_middlename,
            'aws_id': [
                aw.id for aw in aws
                if aw.pc_name == st.session_state.edit_aws
            ][0],
            'server_id': [
                server.server_num for server in servers
                if server.server_name == st.session_state.edit_server
            ][0],
        }

        updated = st.form_submit_button("Обновить линию")
        if updated:
            try:
                CableLineDAO().update(
                    id_x=[
                        cl.id for cl in cable_lines
                        if cl.id == st.session_state.select_cl
                    ][0],
                    data=data
                )
                st.success(
                    'Линия обновлена',
                )
            except Exception as e:
                st.error(f'Ошибка обновления: {e}')

    st.header('Удалить')
    with st.form(key='delete_form'):
        select_cl: list[CableLine] = st.selectbox(
            'Выберите линию',
            options=[cl.id for cl in cable_lines],
            key='delete_cl',
        )
        deleted = st.form_submit_button("Удалить линию")
        if deleted:
            try:
                CableLineDAO().delete(
                    id_x=[
                        cl.id for cl in cable_lines
                        if cl.id == st.session_state.delete_cl
                    ][0]
                )
                st.success(
                    'Линия удалена',
                )
            except Exception as e:
                st.error(f'Ошибка удаления: {e}')
else:
    st.warning(
        'Введен неверный логин или пароль',
    )
