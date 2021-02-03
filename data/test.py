import xlrd, os
folder = "data\\assets"
connect_sign = "\\"

class Member:
    def __init__(self, name, year, excel_index):
        self.name = name
        self.year = year
        self.excel_index = excel_index
        self.shedule = list()
        
    def push_day(self, day):
        self.shedule.append(day)
        
    def push_shedule(self, _):
        self.shedule = _
        
class Day:
    def __init__(self, name):
        self.name = name
        self.shedule = list()
        
    def push_lesson(self, lesson):
        self.shedule.append(lesson)

members = list()
days = ["Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

for grid in os.listdir(folder):

    FILE = folder + connect_sign + grid

    data = xlrd.open_workbook(FILE)

    for i in range(1, len(data.sheet_names())):
        sh1, count = data.sheet_by_index(i), 0
        
        temp_index = 6
        
        if i == 1:
            temp_index = 5
        
        for l in range(sh1.nrows):
            temp_ = sh1.row_values(l)[temp_index]

            if len(str(temp_).split()) == 3:
                members.append(Member(temp_, grid, i))
                
def select_id(name : str):
    identity = None
    
    for member in members:
        if name in member.name:
            identity = member
            break
    
    FILE = "data\\assets" + connect_sign + identity.year
    _, day_counter, checker = xlrd.open_workbook(FILE), -1, 0
    data = _.sheet_by_index(identity.excel_index)  
    
    obj_days = [Day(days[i]) for i in range(len(days))]
    
    for i in range(data.nrows):
        lesson = data.row_values(i)[1]
                                                
        if lesson == "Предмет":
            day_counter += 1
            checker = 0
            
        else:
            if checker < 9 and day_counter != -1:
                if lesson == '':
                    lesson = "окно"
                    
                obj_days[day_counter].push_lesson(lesson)
                checker += 1
                
    identity.push_shedule(obj_days)
    
    return identity