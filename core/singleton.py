# from DAO.aws import AwsDAO
# from DAO.cable_line import CableLineDAO
# from DAO.department import DepartmentDAO
# from DAO.employee import EmployeeDAO
# from DAO.server import ServerDAO
#
#
# class Singleton:
#     __instance = None
#     data: list[object] = []
#
#     @staticmethod
#     def get_instance():
#         """Static access method."""
#         if Singleton.__instance is None:
#             Singleton()
#         return Singleton.__instance
#
#     def __init__(self):
#         """Virtually private constructor."""
#         if Singleton.__instance is not None:
#             raise Exception("This class is a singleton!")
#         else:
#             Singleton.__instance = self
#
#     def add_data(self, dictionaries):
#         """Add a dictionary to the list of data."""
#         self.data = dictionaries
#
#     def get_data(self):
#         """Return the list of data."""
#         return self.data
#
#
# cable_lines = Singleton.get_instance()
# cable_lines.add_data(CableLineDAO().get_all())
# employees = Singleton.get_instance()
# employees.add_data(EmployeeDAO().get_all())
# aws = Singleton.get_instance()
# aws.add_data(AwsDAO().get_all())
# departments = Singleton.get_instance()
# departments.add_data(DepartmentDAO().get_all())
# servers = Singleton.get_instance()
# servers.add_data(ServerDAO().get_all())
