from sqlalchemy import select, update, delete

from DAO.DB.engine import Session, session
from DAO.models import Department
from exceptions import Exceptions


class DepartmentDAO:
    __slots__ = []

    @staticmethod
    def get_all() -> list[Department] | str:
        try:
            statement = select(Department)
            response = session.scalars(statement).all()
            return response
        except Exception as e:
            return Exceptions().get_exception(e)

    @staticmethod
    def add(data: dict) -> None | str:
        try:
            with Session() as conn:
                aws = Department(**data)
                conn.add(aws)
                conn.commit()
        except Exception as e:
            return Exceptions().post_exception(e)

    @staticmethod
    def update(id_x: int, data: dict) -> None | str:
        try:
            statement = update(Department).where(Department.id == id_x) \
                .values(data)
            with Session() as conn:
                conn.execute(statement)
                conn.commit()
        except Exception as e:
            return Exceptions().patch_exception(e)

    @staticmethod
    def delete(id_x: int) -> None | str:
        try:
            statement = delete(Department).where(Department.id == id_x)
            with Session() as conn:
                conn.execute(statement)
                conn.commit()
        except Exception as e:
            return Exceptions().delete_exception(e)
