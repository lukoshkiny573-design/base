from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker


Base = declarative_base()

# Базовый класс для моделей
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


# Подключение к PostgreSQL
DATABASE_URL = "postgresql+psycopg2://postgres:*******@localhost:5432/base" # Пароль скрыл

# Создаю движок
engine = create_engine(DATABASE_URL)

# Создаём все таблицы в БД
Base.metadata.create_all(engine)

print("Таблицы созданы в Postgre")

# Сессия для работы с данными
Session = sessionmaker(bind=engine)
session = Session()

# Пример: добавляю издателя
new_publisher = Publisher(name="Издательство А")
session.add(new_publisher)
session.commit()

print("Издатель добавлен в БД!")

# Закрываю сессию
session.close()

