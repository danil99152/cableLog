from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# путь до БД
database_url = "sqlite:///DAO/DB/cables.db"

# Создание движка подключения
engine = create_engine(database_url)

# Создание сессии для "общения" с нашей бд
Session = sessionmaker(bind=engine)
session = Session()
