from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, PrimaryKeyConstraint, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Teacher(Base):
    __tablename__ = 'Teacher'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    active = Column(Boolean, default=True)
    disciplines = relationship("Discipline",
                               secondary='Competentions',
                               back_populates="teachers")
    shedule = relationship('Shedule', back_populates="teacher")

    def fire(self):
        self.active = False

    def __repr__(self):
        return f'{self.id} - {self.name}'


class Discipline(Base):
    __tablename__ = 'Discipline'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    teachers = relationship("Teacher",
                            secondary='Competentions',
                            back_populates="disciplines")
    service = relationship('Service', back_populates='discipline')

    def __repr__(self):
        return f'{self.id} - {self.name}'


class Service(Base):
    __tablename__ = 'Services'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    discipline_id = Column('Discipline',
                           ForeignKey('Discipline.id'))
    discipline = relationship('Discipline', back_populates='service')
    price = Column(Integer)
    shedule = relationship('Shedule', back_populates="service")

    def update_service(self, name, discipline, price):
        self.name = name
        self.discipline = discipline
        self.price = price

    def __repr__(self):
        return f'{self.name} - {self.discipline}'


association_table = Table('Competentions', Base.metadata,
                          Column('teacher_id', ForeignKey('Teacher.id')),
                          Column('discipline_id', ForeignKey('Discipline.id')),
                          PrimaryKeyConstraint('teacher_id', 'discipline_id')
                          )


class Shedule(Base):
    __tablename__ = 'Shedule'
    date = Column(Date, primary_key=True)
    lesson = Column(Integer, primary_key=True)
    teacher_id = Column('Teacher', ForeignKey('Teacher.id'), primary_key=True)
    service_id = Column('Service', ForeignKey('Services.id'))
    teacher = relationship('Teacher', back_populates='shedule')
    service = relationship('Service', back_populates='shedule')

    def __repr__(self):
        return f'{self.date} - пара:{self.lesson} -'
