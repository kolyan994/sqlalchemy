import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Publisher(Base):
	__tablename__ = 'Publisher'

	id = sq.Column(sq.Integer, primary_key=True)
	name = sq.Column(sq.String(length=40), unique=True)

class Book(Base):
	__tablename__ = 'Book'

	id = sq.Column(sq.Integer, primary_key=True)
	title = sq.Column(sq.String(length=80), unique=True)
	id_publisher = sq.Column(sq.Integer, sq.ForeignKey('Publisher.id'), nullable=False)

	publisher = relationship(Publisher, backref='Book')


class Shop(Base):
	__tablename__ = 'Shop'

	id = sq.Column(sq.Integer, primary_key=True)
	name = sq.Column(sq.String(length=60), unique=True)


class Stock(Base):
	__tablename__ = 'Stock'

	id = sq.Column(sq.Integer, primary_key=True)
	id_book = sq.Column(sq.Integer, sq.ForeignKey('Book.id'), nullable=False)
	id_shop = sq.Column(sq.Integer, sq.ForeignKey('Shop.id'), nullable=False)
	count = sq.Column(sq.Integer)

	book = relationship(Book, backref='Stock')
	shop = relationship(Shop, backref='Shop')


class Sale(Base):
	__tablename__ = 'Sale'

	id = sq.Column(sq.Integer, primary_key=True)
	price = sq.Column(sq.Float)
	date_sale = sq.Column(sq.Date, nullable=False)
	id_stock = sq.Column(sq.Integer, sq.ForeignKey('Stock.id'), nullable=False)
	count = sq.Column(sq.Integer)

	stock = relationship(Stock, backref='Sale')


def create_tables(engine):
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)