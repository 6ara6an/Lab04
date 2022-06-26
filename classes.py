

class Teachers:

    def __init__(self, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class Disciplines:

    def __init__(self, name):
        self.id = id
        self.name = name

    def __str__(self):
        return self.name


class Services:

    def __init__(self, name, discipline, price):
        self.id = id
        self.name = name
        self.discipline = discipline
        self.price = price

    def __str__(self):
        return f'{self.name}/{self.discipline}'



class Shedules:

    def __init__(self, date,lesson, teacher, service ):
        self.date = date
        self.lesson = lesson
        self.teacher = teacher
        self.service = service
    def __str__(self):
        return f'{self.date} - {self.lesson} - {self.teacher} - {self.service}'

class Competentions:

    def __init__(self, teacher, discipline):
        self.teacher = teacher
        self.discipline = discipline


    def __str__(self):
        return f'{self.teacher}/{self.discipline}'