import dearpygui.dearpygui as dpg
from sqlalchemy import create_engine, update, and_
from models import *
from methods import *
from datas import *
from crud import get_session_engine

s, _ = get_session_engine(DATABASE_URI)

query_t = s.query(Teacher).filter(Teacher.active == True)
query_d = s.query(Discipline)
disciplines = query_d.all()
teachers = query_t.all()

dpg.create_context()

with dpg.font_registry():
    with dpg.font("static_data\ARIALN.TTF", 20) as default_font:
        dpg.add_font_range(0x400, 0x4ff)

dpg.create_viewport(title='Task', width=600, height=800)


def hire_fire():
    def update_teachers():
        query_t = s.query(Teacher).filter(Teacher.active == True)
        teachers = query_t.all()
        dpg.configure_item(teachers_list, items=teachers)
        dpg.set_value(item=teachers_list, value='')

    def hire(sender, data, user_data):
        t_data = dpg.get_value(user_data[0])
        t_discipline = dpg.get_value(user_data[1])
        d_id = t_discipline.split('-')[0]
        d = t_discipline.split('-')[1]
        hired = Teacher(name=t_data)
        obj = s.query(Teacher).order_by(Teacher.id.desc()).first()
        t_id = obj.id + 1
        s.add(hired)
        s.commit()
        restart_session()
        comp = association_table.insert().values(teacher_id=t_id, discipline_id=d_id)
        s.execute(comp)
        s.commit()
        restart_session()
        update_teachers()
        dpg.set_value(item=hir, value='Преподаватель ' + t_data + ' принят и будет вести предмет' + d)
        dpg.set_value(item=teacher_data, value='')
        dpg.set_value(item=discipline_list, value='')
        print(f' {hire.__name__} - done')

    def fire(sender, data, user_data):
        chosen = dpg.get_value(user_data[0])
        t_id = chosen.split('-')[0]
        t = chosen.split('-')[1]
        fired = update(Teacher).where(Teacher.id == t_id).values(active=False)
        s.execute(fired)
        s.commit()
        restart_session()
        update_teachers()
        dpg.set_value(item=fir, value='Преподаватель ' + t + ' уволен')
        print(f'{fire.__name__} - done')

    with dpg.window(label="Увольнение", width=600, height=150, autosize=True):
        dpg.bind_font(default_font)
        dpg.add_text("Teachers list")
        teachers_list = dpg.add_combo(label="", items=teachers, width=250)
        dpg.add_button(label="Уволить",
                       callback=fire,
                       user_data=[teachers_list])
        fir = dpg.add_text("")

        teacher_data = dpg.add_input_text(label='ФИО преподавателя')
        discipline_list = dpg.add_combo(label="Предмет", items=disciplines, width=250)
        dpg.add_button(label="Принять",
                       callback=hire,
                       user_data=[teacher_data, discipline_list])
        hir = dpg.add_text("")
    dpg.configure_item(teachers_list, items=teachers)
    dpg.configure_item(discipline_list, items=disciplines)


def service_change():
    query_d = s.query(Discipline)
    dislist = query_d.all()

    def update_services(d_id):
        query_s = s.query(Service).where(Service.discipline_id == d_id).order_by(Service.name)
        # services = query_s.all()
        # dpg.configure_item(teachers_list, items=services)
        dpg.set_value(p1, value=query_s[0].price)
        dpg.set_value(p2, value=query_s[1].price)
        dpg.set_value(p3, value=query_s[2].price)
        dpg.set_value(p4, value=query_s[3].price)

    def get_service_data(sender, data, user_data):
        discipline = dpg.get_value(user_data[0])
        d_id = discipline.split('-')[0]
        d_name = discipline.split('-')[1]
        query_s = s.query(Service).where(Service.discipline_id == d_id).order_by(Service.name)
        dpg.set_value(s1_choosen, value=d_name)
        dpg.set_value(s1, value=query_s[0].name + ' - цена, руб')
        dpg.set_value(s2, value=query_s[1].name + ' - цена, руб')
        dpg.set_value(s3, value=query_s[2].name + ' - цена, руб')
        dpg.set_value(s4, value=query_s[3].name + ' - цена, руб')
        dpg.set_value(p1, value=query_s[0].price)
        dpg.set_value(p2, value=query_s[1].price)
        dpg.set_value(p3, value=query_s[2].price)
        dpg.set_value(p4, value=query_s[3].price)

    def change_sprice(sender, data, user_data):

        serv = []
        for _ in range(4):
            serv.append(int(dpg.get_value(user_data[_])))
        delta_value = dpg.get_value(user_data[4])
        delta_si = dpg.get_value(user_data[5])
        d_id = dpg.get_value(user_data[6]).split('-')[0]
        query_s = s.query(Service).where(Service.discipline_id == d_id).order_by(Service.name)
        new_serv = []
        if delta_value != '':
            if delta_si == '+':
                for x in serv:
                    new_serv.append(x + int(delta_value))
            elif delta_si == '-':
                for x in serv:
                    new_serv.append(x - int(delta_value))
        else:
            for x in serv:
                new_serv.append(x)

        for i in range(len(new_serv)):
            new_serv_price = update(Service).where(Service.discipline_id == d_id,
                                                   Service.name == query_s[i].name).values(
                price=new_serv[i])
            s.execute(new_serv_price)
            s.commit()
            restart_session()
            update_services(d_id)

        print(new_serv)

    with dpg.window(label="Услуги", width=600, height=600):
        dpg.bind_font(default_font)
        dpg.add_text("Изменение услуг")
        disc_list = dpg.add_combo(label="Выберите предмет", items=dislist, width=250)

        dpg.add_button(label="Выбрать",
                       callback=get_service_data,
                       user_data=[disc_list, service_names])
        s1_choosen = dpg.add_text("")

        s1 = dpg.add_text("")
        p1 = dpg.add_input_text(width=100)
        s2 = dpg.add_text("")
        p2 = dpg.add_input_text(width=100)
        s3 = dpg.add_text("")
        p3 = dpg.add_input_text(width=100)
        s4 = dpg.add_text("")
        p4 = dpg.add_input_text(width=100)

        radio = delta_sign = dpg.add_radio_button(label='Изменение цены', items=['+', '-'], horizontal=True)
        delta = dpg.add_input_text(label='Сумма изменения для всех услуг', width=100)
        dpg.add_button(label="Изменить",
                       callback=change_sprice,
                       user_data=[p1, p2, p3, p4, delta, delta_sign, disc_list])

        dpg.configure_item(radio, item='+')
        dpg.configure_item(disc_list, items=dislist)


def shedule_change():
    les = []
    for n, time in lessons.items():
        les.append(f'{n} - {time}')

    query_t = s.query(Teacher).filter(Teacher.active == True)
    teachers = query_t.all()
    shedule = []
    disc = []

    def update_shedules(t_id):
        query_sh = s.query(Shedule, Service.name).join(Service).filter(and_(Shedule.teacher_id == t_id,
                                                                            Service.id == Shedule.service_id))
        shedule = query_sh.all()
        dpg.configure_item(shedue_t, items=shedule)

    def get_shedule_data(sender, data, user_data):
        t_id = dpg.get_value(user_data[0]).split('-')[0]
        query_sh = s.query(Shedule, Service.name).join(Service).filter(and_(Shedule.teacher_id == t_id,
                                                                            Service.id == Shedule.service_id))
        query_d_c = s.query(Discipline).join(association_table).filter(association_table.c.teacher_id == t_id)
        disc = [y for y in query_d_c.all()]
        shedule = query_sh.all()
        dpg.configure_item(shedue_t, items=shedule)
        dpg.configure_item(discipline, items=disc)

    def create_shedule_row(sender, data, user_data):
        t_id = dpg.get_value(user_data[3]).split('-')[0]
        s_id = s.query(Service).filter(Service.name == dpg.get_value(user_data[2]).split('-')[0],
                                       Service.discipline_id == dpg.get_value(user_data[4]).split('-')[0])[0].id
        date = dpg.get_value(user_data[0])
        norm_date = f'{date["year"] + 1900}-{"0" + str(date["month"] + 1)}-{"0" + str(date["month_day"])}'
        less = dpg.get_value(user_data[1]).split('-')[0]
        new_row = Shedule(date=norm_date, lesson=less, teacher_id=t_id, service_id=s_id)
        s.add(new_row)
        s.commit()
        restart_session()
        update_shedules(t_id)

    with dpg.window(label="График", width=600, height=600):
        dpg.bind_font(default_font)
        dpg.add_text("Teachers list")
        teach_list = dpg.add_combo(label="", items=teachers, width=250)
        dpg.add_button(label="Выбрать",
                       callback=get_shedule_data,
                       user_data=[teach_list])
        dpg.add_text("График преподавателя")
        shedue_t = dpg.add_listbox(items=shedule)
        date = dpg.add_date_picker(default_value={'year': 22})
        lesson = dpg.add_combo(items=les)
        discipline = dpg.add_combo(items=disc)
        service = dpg.add_combo(items=service_names)
        dpg.add_button(label="Добавить",
                       callback=create_shedule_row,
                       user_data=[date, lesson, service, teach_list, discipline])

    dpg.configure_item(teach_list, items=teachers)


with dpg.window(label="Действия", width=600, height=200, autosize=True):
    dpg.bind_font(default_font)
    dpg.add_button(label="Прием/Увольнение",
                   callback=hire_fire)
    dpg.add_button(label="Услуги",
                   callback=service_change)
    dpg.add_button(label="График",
                   callback=shedule_change)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
