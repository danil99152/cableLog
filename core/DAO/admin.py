from sqlalchemy import select

from DAO.DB.engine import Session, session
from DAO.models import Admin
from exceptions import Exceptions


class AdminDAO:
    __slots__ = []

    @staticmethod
    def get(index: int) -> list[Admin] | str:
        try:
            statement = select(Admin).where(Admin.id == index)
            response = session.scalars(statement).all()
            return response
        except Exception as e:
            return Exceptions().get_exception(e)

    @staticmethod
    def add(data: dict) -> None | str:
        try:
            with Session() as conn:
                aws = Admin(**data)
                conn.add(aws)
                conn.commit()
        except Exception as e:
            return Exceptions().post_exception(e)
