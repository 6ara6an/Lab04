from config import DATABASE_URI
from models import *
from crud import get_session_engine
from sqlalchemy import and_, update

s, _ = get_session_engine(DATABASE_URI)


def shedule_service_check(t_id, s_id):
    query_c = s.query(association_table).filter(association_table.c.teacher_id == t_id)
    c_d_ids = [x.discipline_id for x in query_c]
    query_s = s.query(Service).filter(and_(Service.discipline_id.in_(c_d_ids), Service.id == s_id))
    if len(query_s.all()) == 0:
        return False
    return True


def shedule_add(date, lesson, t_id, s_id):
    query_s = s.query(Shedule).filter(and_(Shedule.teacher_id == t_id,
                                           Shedule.lesson == lesson),
                                      Shedule.date == date)
    if len(query_s.all()) != 0:
        print('Преподаватель занят в это время')
        return False

    check = shedule_service_check(t_id, s_id)
    if check:
        shed = Shedule(date=date, lesson=lesson, teacher_id=t_id, service_id=s_id)
        s.add(shed)
        print('Запись внесена в расписание')
        return True
    else:
        print('Преподаватель не может провести эту пару')
        return False


def shedule_change(date, lesson, t_id, s_id, new_t_id, new_s_id):
    query_s = s.query(Shedule).filter(and_(Shedule.teacher_id == t_id,
                                           Shedule.lesson == lesson,
                                           Shedule.date == date,
                                           Shedule.service_id == s_id))
    if len(query_s.all()) == 0:
        print('Такой записи нет')
        return False

    check = shedule_service_check(new_t_id, new_s_id)
    if check:
        new_row = update(Shedule).where(and_(Shedule.teacher_id == t_id,
                                             Shedule.lesson == lesson,
                                             Shedule.date == date,
                                             Shedule.service_id == s_id)).values(
            Shedule.teacher_id == new_t_id,
            Shedule.lesson == lesson,
            Shedule.date == date,
            Shedule.service_id == new_s_id)
        s.execute(new_row)
        print('Запись изменена')
        return True
    else:
        print('Преподаватель не может провести эту пару')
        return False


shedule_add('2022-05-06', 6, 1, 24)

s.commit()
