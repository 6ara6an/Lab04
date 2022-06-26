from config import DATABASE_URI
from models import *
from crud import get_session_engine
from sqlalchemy import and_, update

s, _ = get_session_engine(DATABASE_URI)


def list_of_services(start_date, last_date, t_id):
    query_s = s.query(Shedule, Service).filter(and_(Shedule.teacher_id == t_id,
                                           Shedule.date >= start_date,
                                           Shedule.date <= last_date)).join(Service, Service.id == Shedule.service_id)

    teacher_name = (s.query(Teacher).filter(Teacher.id == query_s[0][0].teacher_id))[0].name
    queryset = query_s.all()
    sums = [x.price for z, x in queryset]
    print('Ведомость оказанных услуг')
    print('__________________________________________________')
    print(f'Преподаватель: {teacher_name}')
    print(f'Отчетный период: с {start_date} по {last_date}')
    print('__________________________________________________')
    print(f'Оказано услуг: {len(queryset)}')
    print(f'На сумму: {sum(sums)}')

list_of_services('2022-05-01', '2022-05-30', 1)

s.commit()
