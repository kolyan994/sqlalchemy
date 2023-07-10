import json
import os
from dotenv.main import load_dotenv
import sqlalchemy
from sqlalchemy.orm import sessionmaker

from models import create_tables, Publisher, Shop, Book, Stock, Sale

load_dotenv()  # загружаем данные из .env файла

login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')
bdname = os.getenv('BDNAME')
port = os.getenv('PORT')
host = os.getenv('HOST')

DSN = f'postgresql://{login}:{password}@{host}:{port}/{bdname}'
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)  # Удаляем старые и создаем новые таблицы


def find_sales(session,pub):  # Функция, выводящая итоговый результат
    selected = session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher).join(Stock).join(Shop).join(Sale).filter(Publisher.name == pub)
    for s in selected.all():
        print(f"{s[0]} | {s[1]} | {s[2]} | {s[3]}")


Session = sessionmaker(bind=engine)
session = Session()

#  Загружаем данные в БД из json
with open('test_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()
session.close()

if __name__ == '__main__':
    pub = 'O’Reilly'  # Вместо инпута прописываем название автора сюда
    find_sales(session, pub)  # Вызываем итоговую функцию


