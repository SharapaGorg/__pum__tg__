import xlrd, sys

members = list()

if sys.platform == "win32" : spliter = "\\"
else: spliter = "/"

if __name__ == "__main__":
    from utils import Day, Lesson
    from utils import filler
    folder = "assets" + spliter
else:
    from data.utils import Day, Lesson
    from data.utils import filler
    folder = "data" + spliter + "assets" + spliter
   
filler(folder, members, 8, 7, {5 : 6} , 0)         # fill 8 course
filler(folder, members, 9, 6, {0 : 7}, 24)         # fill 9 course
filler(folder, members, 10, 6, {}, 9)              # fill 10 course
filler(folder, members, 11, 6, {9 : 7, 11 : 7}, 0) # fill 11 course
            
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]

def select_id(name : str):
    """
    :return: Расписание ученика
    """
    
    identity = None
    
    for member in members:
        if name.lower() in member.name.lower():
            identity = member
            break
    
    FILE = f"data{spliter}assets{spliter}{identity.year}"
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

                elif 'зал' in str(cabinet):
                    cabinet = 'зал'
                    
                obj_lesson = Lesson(lesson, group, cabinet, teacher)
                
                for i in range(len(obj_days)):
                    if obj_days[i].name.lower() == temp_day.lower():
                        obj_days[i].push_lesson(obj_lesson)
                  
                checker += 1
                
    identity.push_shedule(obj_days)
    
    return identity
