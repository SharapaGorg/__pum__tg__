import xlrd, sys
import json

if sys.platform == "win32" : spliter = "\\"
else: spliter = "/"

if __name__ == "__main__":
    folder = "assets" + spliter
else:
    folder = "data" + spliter + "assets" + spliter

class Member:
    def __init__(self, name, year, excel_index):
        self.name = name
        self.year = str(year) + ".xlsx"
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
        
    def push_day_shedule(self, day_shedule):
        self.shedule = day_shedule
        
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
            raise Exception("-")

days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

def is_indentity( name_object : str ) -> bool:
    return name_object != '' and len(name_object.split()) == 3

def capital_reg(word : str) -> str:
    return word[0].upper() + word[1:]

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def filler( source : str, members : list, course : int, active : int, unusual_positions : dict, *pass_index):
    """
    
    course - school course of education of student
    active - active rows in every excel_index
    pass_index - excel_index without student`s names 
    unusual_positions - { <excel_index , that has some changes> : <new_active_row> }
    
    P.S : active_rows - rows in every excel_index, that have student`s names
    
    """
    
    SOURCE = source + str(course) + ".xlsx"
    data = xlrd.open_workbook(SOURCE)
    pass_index = list(pass_index)
    
    for i in range(len(data.sheet_names())):
        sh1, temp_active, accept_handling = data.sheet_by_index(i), active, 1
        
        for k in range(len(pass_index)): # checking for junk excel_index list
            if pass_index[k] == i:
                accept_handling = 0
                pass_index.remove(pass_index[k])
                break
         
        if not accept_handling: 
            continue
        
        for elem in unusual_positions: # checking for unusual changes in course.xlsx
            if i == elem:
                temp_active = unusual_positions[elem]
        
        for j in range(sh1.nrows):
            try:
                identity = sh1.row_values(j)[temp_active]
                _course = course
                index_of_excel_table = i
                
                if is_indentity (identity): # checking for correctly writing
                    members.append(Member(identity, _course, index_of_excel_table))
                    
            except: pass
            
def item_list() -> list:
    container = list()
    FILE = f"data{spliter}assets{spliter}9.xlsx"
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

def return_static_shedule(container : list, folder_ : str) -> list:
    """

    :return:
    
    Object arch shedule ->
    
    [
        Member ->
                - Member.name
                - Member.year
                - Member.excel_index
                - Member.shedule ->
                    [
                        Day  ->
                                - Day.name
                                - Day.shedule -> 
                                    [
                                        Lesson -> 
                                                - Lesson.name
                                                - Lesson.group
                                                - Lesson.teacher
                                                - Lesson.cabinet
                                        ...
                                    ]
                        ...
                    ]
        ...
    ]

    """

    DATA = list() # list type of : [Member.shedule = Day.shedule = [Lesson(...) * len(list)]]
    
    for student in container:
        print(student.name)
        
        student_shedule, temp_day,  access = list(), list(), False
        
        src_path = folder_ + student.year
        SRC = xlrd.open_workbook(src_path)
        
        shedule_index = SRC.sheet_by_index(student.excel_index)
        
        for i in range(shedule_index.nrows):     
            day = shedule_index.row_values(i)[0]
            lesson = shedule_index.row_values(i)[1]
            group = shedule_index.row_values(i)[2]
            teacher = shedule_index.row_values(i)[3]
            cabinet = shedule_index.row_values(i)[4]  
            
            if access:
                temp_day.append(Lesson(lesson, group, cabinet, teacher))
            
            if day in days:
                _day = Day(day)
                _day.push_day_shedule(temp_day)
                
                student_shedule.append(_day)
                
                temp_day = list()                    
                access = True
                
        DATA.append(student_shedule)
        
    return DATA
        
def telegram_shedule(object_shedule : list):
    """
    
    :return:
    
    String arch shedule instead Object arch shedule ->
    
    [
        {
            Member.name : 
                    [
                        {
                            Day.name : 
                                    [
                                        Lesson.name,
                                        Lesson.name,
                                        Lesson.name,
                                        ...
                                    ]
                        },
                            Day.name : 
                                    [
                                        Lesson.name,
                                        Lesson.name,
                                        Lesson.name,
                                        ...
                                    ],
                            ...
                    ]
        },
        ...
        
    ]
    
    """
                
def write_list_to_json(data_list : list, filename : str):
    with open(filename, "w", encoding = "utf-8") as wrote:
        target = str(data_list)
        