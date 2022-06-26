from config import DATABASE_URI
from models import *
from crud import get_session_engine
from sqlalchemy import update


s, _ = get_session_engine(DATABASE_URI)


def change_price(sum, id, sign='+'):
    query_d = s.query(Discipline).filter(Discipline.id == id)
    query_t = s.query(Service).filter(Service.discipline_id == id)
    print(f'Цена на услуги по предмету "{query_d[0]}" увеличена на {sum}.')
    print('Новые цены:')
    for q in query_t:
        if sign == '-':
            price = q.price - sum
        else:
            price = q.price + sum
        new_price = update(Service).where(Service.id == q.id).values(price=price)
        s.execute(new_price)
        print(f'{q} = {price}')

s.commit()