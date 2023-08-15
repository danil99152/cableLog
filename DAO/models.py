from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase


# Использование создания basemodel до sqlalchemy 2.0.0
# Base = declarative_base()

# Использование создания basemodel после sqlalchemy 2.0.0
class Base(DeclarativeBase):
    pass


class Server(Base):
    __tablename__ = 'servers'

    server_num = Column(Integer, primary_key=True, index=True)
    server_name = Column(String(50), unique=True)


class Department(Base):
    __tablename__ = 'departments'

    id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(50), unique=True)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String(50))
    name = Column(String(50))
    middlename = Column(String(50))
    department_id = Column(Integer, ForeignKey('departments.id'), index=True)

    department = relationship(Department, backref='employees')

    @property
    def full_name(self) -> str:
        return f'{self.surname} {self.name} {self.middlename}'


class AWS(Base):
    __tablename__ = 'aws'

    id = Column(Integer, primary_key=True, index=True)
    pc_name = Column(String(50), unique=True)
    ip = Column(String(15), unique=True)
    mac = Column(String(17), unique=True)

    employee_id = Column(Integer, ForeignKey('employees.id'), index=True)
    employee = relationship(Employee, backref='cable_lines')


class CableLine(Base):
    __tablename__ = 'cable_lines'

    id = Column(Integer, primary_key=True, index=True)
    socket_num = Column(Integer)
    socket_port = Column(Integer)
    patchpanel_port = Column(Integer)
    length = Column(Integer)

    aws_id = Column(Integer, ForeignKey('aws.id'), index=True)
    aws = relationship(AWS, backref='cable_lines')

    server_id = Column(Integer, ForeignKey('servers.server_num'), index=True)
    server = relationship(Server, backref='cable_lines')


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True)
    password = Column(String(50), unique=True)
