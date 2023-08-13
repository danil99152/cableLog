from sqlalchemy import select, update, delete

from DAO.DB.engine import Session, session
from DAO.models import Employee
from exceptions import Exceptions


class EmployeeDAO:
    __slots__ = []

    @staticmethod
    def get_all() -> list[Employee] | str:
        try:
            statement = select(Employee)
            response = session.scalars(statement).all()
            return response
        except Exception as e:
            return Exceptions().get_exception(e)

    @staticmethod
    def add(data: dict) -> None | str:
        try:
            with Session() as conn:
                aws = Employee(**data)
                conn.add(aws)
                conn.commit()
        except Exception as e:
            return Exceptions().post_exception(e)

    @staticmethod
    def update(id_x: int, data: dict) -> None | str:
        try:
            statement = update(Employee).where(Employee.id == id_x) \
                .values(data)
            with Session() as conn:
                conn.execute(statement)
                conn.commit()
        except Exception as e:
            return Exceptions().patch_exception(e)

    @staticmethod
    def delete(id_x: int) -> None | str:
        try:
            statement = delete(Employee).where(Employee.id == id_x)
            with Session() as conn:
                conn.execute(statement)
                conn.commit()
        except Exception as e:
            return Exceptions().delete_exception(e)
