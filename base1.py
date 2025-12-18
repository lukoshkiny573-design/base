from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from datetime import datetime

# 1. Создаём базовый класс для моделей
Base = declarative_base()

# 2. Определяем модели данных (таблицы БД)
class Publisher(Base):
    __tablename__ = 'publisher'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    books = relationship("Book", back_populates="publisher")

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'))
    publisher = relationship("Publisher", back_populates="books")
    stocks = relationship("Stock", back_populates="book")

class Shop(Base):
    __tablename__ = 'shop'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    stocks = relationship("Stock", back_populates="shop")
    sales = relationship("Sale", back_populates="shop")

class Stock(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'))
    id_shop = Column(Integer, ForeignKey('shop.id'))
    count = Column(Integer, nullable=False)
    book = relationship("Book", back_populates="stocks")
    shop = relationship("Shop", back_populates="stocks")
    sales = relationship("Sale", back_populates="stock")

class Sale(Base):
    __tablename__ = 'sale'
    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    date_sale = Column(DateTime, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'))
    count = Column(Integer, nullable=False)
    stock = relationship("Stock", back_populates="sales")
    id_shop = Column(Integer, ForeignKey('shop.id'))
    shop = relationship("Shop", back_populates="sales")


# 3. Подключение к БД (PostgreSQL)
DATABASE_URL = "postgresql+psycopg2://postgres:alina2020@localhost:5432/base"
engine = create_engine(DATABASE_URL)

# Создаём сессию
Session = sessionmaker(bind=engine)
session = Session()

# 4. Получаем имя или ID издателя от пользователя
publisher_input = input("Введите имя или ID издателя: ")

# 5. Формируем запрос для выборки фактов покупки книг данного издателя
if publisher_input.isdigit():  # Если введён ID
    sales = session.query(Sale, Book, Shop).join(
        Stock, Sale.id_stock == Stock.id
    ).join(
        Book, Stock.id_book == Book.id
    ).join(
        Shop, Stock.id_shop == Shop.id
    ).filter(
        Book.id_publisher == int(publisher_input)
    ).all()
else:  # Если введено имя
    sales = session.query(Sale, Book, Shop).join(
        Stock, Sale.id_stock == Stock.id
    ).join(
        Book, Stock.id_book == Book.id
    ).join(
        Shop, Stock.id_shop == Shop.id
    ).join(
        Publisher, Book.id_publisher == Publisher.id
    ).filter(
        Publisher.name == publisher_input
    ).all()

# 6. Выводим результаты построчно в требуемом формате
print("название книги | название магазина | стоимость покупки | дата покупки")
for sale, book, shop in sales:
    print(f"{book.title} | {shop.name} | {sale.price} | {sale.date_sale.strftime('%d-%m-%Y')}")

# 7. Закрываем сессию
session.close()
