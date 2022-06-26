# CRUD = Create, Read, Update, Delete
from sqlalchemy import create_engine
from config import DATABASE_URI
from models import *
from sqlalchemy.orm import scoped_session, sessionmaker


def get_session_engine(db_uri):
    engine = create_engine(db_uri)
    session = scoped_session(sessionmaker(bind=engine))
    return session, engine


def create_database(db_uri):
    session, engine = get_session_engine(db_uri)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    return session


def fill_db(session):
    def read_csv(name):
        with open(f'./static_data/{name}.csv', 'r', encoding='utf8') as f:
            result = [line.strip() for line in f]
        return result

    teachers = read_csv('teachers')
    disciplines = read_csv('disciplines')

    for t in teachers:
        teacher = Teacher(name=t)
        session.add(teacher)

    for d in disciplines:
        discipline = Discipline(name=d)
        session.add(discipline)

    session.commit()


if __name__ == '__main__':
    print('connecting...')

    session = create_database(DATABASE_URI)

    fill_db(session)
    print('db created!')

    session.close()
    print('session closed')
