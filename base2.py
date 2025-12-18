import json
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables, Publisher, Shop, Book, Stock, Sale  # предполагаем, что модели в файле models.py

# Подключение к БД
DSN = "postgresql+psycopg2://postgres:******@localhost:5432/base"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)  # создаём таблицы, если их нет

# Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()

# Читаем JSON-файл
with open('fixtures/tests_data.json', 'r') as fd:
    data = json.load(fd)

# Загружаем данные в БД
for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))

# Сохраняем изменения
session.commit()
session.close()
print("Данные загружены!")
