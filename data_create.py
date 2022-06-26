from random import randint, shuffle
from config import DATABASE_URI
from models import *
from datas import *
from crud import get_session_engine


s, _ = get_session_engine(DATABASE_URI)

query_t = s.query(Teacher)
query_d = s.query(Discipline)

# создаем Услуги (Service)
def fill_services(query_d, service_names ):
    for d in query_d:
        for sn in service_names:
            name = sn
            discipline = d.id
            price = randint(2000, 5000)
            service = Service(name=name, discipline_id=discipline, price=price)
            s.add(service)


# создаем случайные Компетенции
def fill_competention(query_t, query_d):
    for t in query_t:
        i = 1
        qs = query_d.all()
        while i != 4:
            shuffle(qs)
            d_id = qs.pop().id
            i += 1
            t_id = t.id
            comp = association_table.insert().values(teacher_id=t_id, discipline_id=d_id)
            s.execute(comp)


fill_services(query_d, service_names)
fill_competention(query_t, query_d)

s.commit()
