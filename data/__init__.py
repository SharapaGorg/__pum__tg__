import xlrd, os, sys

if sys.platform == "win32":
    connect_sign = "\\"
else:
    connect_sign = "/"

folder = "data" + connect_sign + "assets"

def capital_reg(word : str) -> str:
    return word[0].upper() + word[1:]

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
        
    def __str__(self) -> str:
        return self.name[0] + self.name[1:]
        
class Day:
    def __init__(self, name):
        self.name = name
        self.shedule = list()
        
    def push_lesson(self, lesson):
        self.shedule.append(lesson)
        
    def __str__(self) -> str:
        return self.name[0] + self.name[1:]
    
class Lesson:
    def __init__(self, name, group : str, cab : str, teacher : str):
        try:
            self.cab = str(int(float(cab)))
        except:
            self.cab = cab
            
        self.name = name
        self.group = group
        self.teacher = teacher
        
    def __str__(self) -> str:
        try:
            return self.name[0].upper() + self.name[1:]
        except:
            #stupid bug
            raise Exception("Psevdo window in shedule [-]")
                
members = list()
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

for grid in os.listdir(folder):

    FILE = folder + connect_sign + grid

    data = xlrd.open_workbook(FILE)

    for i in range(0, len(data.sheet_names())):
        sh1, count = data.sheet_by_index(i), 0
        
        temp_index = 6
        
        if grid == '8.xlsx':
            temp_index = 7
 
        if i == 0 and grid == '9.xlsx':
            temp_index = 7
        if i == 5 and grid == '8.xlsx':
            temp_index = 6
        if i == 9 or i == 11 and grid == '11.xlsx':
            temp_index = 7
        
        for l in range(sh1.nrows):
            try:
                temp_ = sh1.row_values(l)[temp_index]

                if len(str(temp_).split()) == 3:
                    members.append(Member(temp_, grid, i))
            except : pass

def select_id(name : str):
    """
    :return: Расписание ученика
    """
    
    identity = None
    
    for member in members:
        if name.lower() in member.name.lower():
            identity = member
            break
    
    FILE = f"data{connect_sign}assets{connect_sign}{identity.year}"
    _, day_counter, checker = xlrd.open_workbook(FILE), -1, 0
    data = _.sheet_by_index(identity.excel_index)  
    
    obj_days = [Day(days[i]) for i in range(len(days))]
    temp_day = ""
     
    for i in range(data.nrows):
        lesson = data.row_values(i)[1]
        group = data.row_values(i)[2]
        teacher = data.row_values(i)[3]
        cabinet = data.row_values(i)[4]
        
        for elem in obj_days:
            if str(data.row_values(i)[0]).lower() == elem.name.lower():
                temp_day = elem.name
                                              
        if lesson == "Предмет":
            day_counter += 1
            checker = 0
            
        else:
            if checker < 9 and day_counter != -1:
                if lesson == '' and data.row_values(i)[0] != '' and data.row_values(i)[0] not in days:
                    lesson = "окно"
                    
                    print(temp_day)
                elif 'зал' in str(cabinet):
                    cabinet = 'зал'
                    
                obj_lesson = Lesson(lesson, group, cabinet, teacher)
                
                for i in range(len(obj_days)):
                    if obj_days[i].name.lower() == temp_day.lower():
                        obj_days[i].push_lesson(obj_lesson)
                  
                checker += 1
                
    for elem in obj_days:
        print(elem.shedule)
                
    identity.push_shedule(obj_days)
    
    return identity

def item_list() -> list:
    container = list()
    FILE = f"data{connect_sign}assets{connect_sign}9.xlsx"
    _ = xlrd.open_workbook(FILE)
    data = _.sheet_by_index(1)
    names = list()
    
    for i in range(data.nrows):
        lesson = data.row_values(i)[1]
        group = data.row_values(i)[2]
        teacher = data.row_values(i)[3]
        cabinet = data.row_values(i)[4]    
        
        if lesson != "Предмет" and lesson != ' ':
            __obj_lesson = Lesson(lesson, group, cabinet, teacher)
            
            if lesson not in names:
                container.append(__obj_lesson)
                names.append(lesson)
            
    result = set(container)
            
    return result

import json

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def select_item(**item_info):
    with open(f"data{connect_sign}latest_shedule.json", "r", encoding = "utf-8") as handled:
        data = json.loads(handled.readline())
        res = set()
        
        for member in data:
            for day in member.values():
                for item_kit in day.values():
                    for item in item_kit:
                        if item.upper() == item_info['item'].upper() and item_kit.index(item) + 1 == item_info['index'] and get_key(day, item_kit).upper() == item_info['day'].upper():
                            for key in member.keys():
                                res.add(key)
    
        if len(res) != 0:
            return res
        else:
            raise Exception("NotFoundImportantInfo")