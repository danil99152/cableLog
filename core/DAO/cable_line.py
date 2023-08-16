from sqlalchemy import select, update, delete

from DAO.DB.engine import Session, session
from DAO.models import CableLine
from exceptions import Exceptions


class CableLineDAO:
    __slots__ = []

    @staticmethod
    def get_all() -> list[CableLine] | str:
        try:
            statement = select(CableLine)
            response = session.scalars(statement).all()
            return response
        except Exception as e:
            return Exceptions().get_exception(e)

    @staticmethod
    def add(data: dict) -> None | str:
        try:
            with Session() as conn:
                cable_line = CableLine(**data)
                conn.add(cable_line)
                conn.commit()
        except Exception as e:
            return Exceptions().post_exception(e)

    @staticmethod
    def update(id_x: int, data: dict) -> None | str:
        try:
            statement = update(CableLine).where(CableLine.id == id_x) \
                .values(data)
            with Session() as conn:
                conn.execute(statement)
                conn.commit()
        except Exception as e:
            return Exceptions().patch_exception(e)

    @staticmethod
    def delete(id_x: int) -> None | str:
        try:
            statement = delete(CableLine).where(CableLine.id == id_x)
            with Session() as conn:
                conn.execute(statement)
                conn.commit()
        except Exception as e:
            return Exceptions().delete_exception(e)
