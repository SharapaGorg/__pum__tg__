from threading import current_thread
import xlrd, sys, os

if sys.platform == "win32" : spliter = "\\"
else: spliter = "/"

try: from constants import bells_8_9, bells_10_11, data_file
except: from data.constants import bells_8_9, bells_10_11, data_file

if __name__ == "__main__":
    folder = "assets" + spliter
else:
    folder = "data" + spliter + "assets" + spliter

window_counter = 0
temp_group = str()

class Day:
    def __init__(
        self,
        title : str
    ):

        self.title = title
        self.shedule = list()

    def update_shedule(self, lesson):
        self.shedule.append(lesson)

    def __str__(self):
        return self.title

class Week:
    def __init__(
        self):

        self.shedule = list()

    def update_shedule(self, lesson):
        self.shedule.append(lesson)

    def __str__(self):
        return '<Week shedule>'

class Lesson:
    def __init__(self, 
                title : str, 
                group : str, 
                teacher : str, 
                cab : str, 
                bell = '00:00'):

        self.title = title
        self.group = group
        self.teacher = teacher
        self.cab = str(cab).rstrip('.0') if str(cab) != 'спортзал' else 'зал'
        self.bell = bell

    def __str__(self):
        return self.title

class StudentShedule:
    def __init__(self, name : str):
        self.name = name
        self.shedule = dict()
        self.window_checker = 0

        __week = Week()
        __day = None

        SOURCE = 'data' + spliter + data_file

        is_found = False
        for student in os.listdir(SOURCE):
            if name in student:
                self.name = student.rstrip('.xlsx')
                is_found = True

                data =  xlrd.open_workbook(SOURCE + spliter + student).sheet_by_index(0)

                counter = 0
                for i in range(data.nrows):
                    if counter == 14: 
                        counter = 0

                    first_col = data.row_values(i)[0]
                    second_col = data.row_values(i)[1] # subject title
                    third_col = data.row_values(i)[2]  # group title
                    fourth_col = data.row_values(i)[3] # teacher name
                    fifth_col = data.row_values(i)[4]  # cabinet number

                    if "8" in third_col or "9" in third_col or "10" in third_col or "11" in third_col:
                        temp_group = third_col.split('-')[1]

                    if counter == 0:
                        if __day : 
                            __week.update_shedule(__day)

                        __day = Day(first_col)
                    if counter == 1: pass
                    else: 
                        _lesson = Lesson(second_col, third_col, fourth_col, fifth_col)
                        __day.update_shedule(_lesson)

                    counter += 1

                __week.update_shedule(__day)

                for day in __week.shedule:
                    (day.shedule).remove(day.shedule[0])

                    checker = False
                    for i in range(len(day.shedule) - 1, 0, -1):
                        lesson = day.shedule[i]

                        if (len(lesson.title) == 0 and not checker):
                            day.shedule.remove(lesson)

                        if (len(lesson.title) == 0 and checker):
                            self.window_checker += 1

                        if (len(lesson.title) > 0):
                            checker = True

                    for i in range(len(day.shedule)):
                        if temp_group == '9' or temp_group == '8':
                            day.shedule[i].bell = bells_8_9[i]

                        if temp_group == '10' or temp_group == '11':
                            day.shedule[i].bell = bells_10_11[i]
                            
                self.shedule = __week.shedule

                break      

        if not is_found:
            raise Exception('Student not found')

    def __str__(self):
        return self.name