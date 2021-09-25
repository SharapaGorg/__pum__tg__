import xlrd
import sys
import os

if sys.platform == "win32":
    spliter = "\\"
else:
    spliter = "/"

try:
    from constants import bells_8_9, bells_10_11, assets_folder, static_folder
except:
    from data.constants import bells_8_9, bells_10_11, assets_folder, static_folder

if __name__ == "__main__":
    folder = "assets" + spliter
else:
    folder = "data" + spliter + "assets" + spliter

temp_group = str()


class Day:
    def __init__(
        self,
        title: str
    ):

        self.title = title
        self.schedule = list()

    def update_schedule(self, lesson):
        self.schedule.append(lesson)

    def __str__(self):
        return self.title


class Week:
    def __init__(
            self):

        self.schedule = list()

    def update_schedule(self, lesson):
        self.schedule.append(lesson)

    def __str__(self):
        return '<Week schedule>'


class Lesson:
    def __init__(self,
                 title: str = 'Окно',
                 group: str = '',
                 teacher: str = '?',
                 cab: str = '000',
                 bell='00:00'):

        self.title = title
        self.group = group
        self.teacher = teacher
        self.cab = str(cab).rstrip('.0') if str(cab) != 'спортзал' else 'зал'
        self.bell = bell

    def __str__(self):
        return self.title


class StudentSchedule:
    def __init__(self, name: str):
        self.name = name
        self.schedule = dict()
        self.window_checker = 0

        __week = Week()
        __day = None

        SOURCE = 'data' + spliter + assets_folder

        is_found = False
        for student in os.listdir(SOURCE):
            if name in student:
                self.name = student.rstrip('.xlsx')
                is_found = True

                data = xlrd.open_workbook(
                    SOURCE + spliter + student).sheet_by_index(0)

                counter = 0
                for i in range(data.nrows):
                    if counter == 14:
                        counter = 0

                    first_col = data.row_values(i)[0]
                    second_col = data.row_values(i)[1]  # subject title
                    third_col = data.row_values(i)[2]  # group title
                    fourth_col = data.row_values(i)[3]  # teacher name
                    fifth_col = data.row_values(i)[4]  # cabinet number

                    if "8" in third_col or "9" in third_col or "10" in third_col or "11" in third_col:
                        temp_group = third_col.split('-')[1]

                    if counter == 0:
                        if __day:
                            __week.update_schedule(__day)

                        __day = Day(first_col)
                    if counter == 1:
                        pass
                    else:
                        _lesson = Lesson(second_col, third_col,
                                         fourth_col, fifth_col)
                        __day.update_schedule(_lesson)

                    counter += 1

                __week.update_schedule(__day)

                for day in __week.schedule:
                    (day.schedule).remove(day.schedule[0])

                    checker = False
                    for i in range(len(day.schedule) - 1, 0, -1):
                        lesson = day.schedule[i]

                        if (len(lesson.title) == 0 and not checker):
                            day.schedule.remove(lesson)

                        if (len(lesson.title) == 0 and checker):
                            self.window_checker += 1

                        if (len(lesson.title) > 0):
                            checker = True

                    for i in range(len(day.schedule)):
                        if temp_group == '9' or temp_group == '8':
                            day.schedule[i].bell = bells_8_9[i]

                        if temp_group == '10' or temp_group == '11':
                            day.schedule[i].bell = bells_10_11[i]

                self.schedule = __week.schedule

                break

        if not is_found:
            raise Exception('Student not found')

    def __str__(self):
        return self.name


class Teacher:
    __title__ = 'Teacher'
    __folder__ = 'data' + spliter + assets_folder

    __TEACHERS = dict()
    _schedule = None

    def __init__(self, name, *args):
        self._name = name
        self.args = args

    def __update(self):
        """
        Update teacher`s schedule and fill with new information
        base on all students schedule
        """

        for student in os.listdir(self.__folder__):
            student_schedule = xlrd.open_workbook(
                self.__folder__ + spliter + student).sheet_by_index(0)

            day_title = str()

            for i in range(student_schedule.nrows):

                first_column = student_schedule.row_values(
                    i)[0]  # number of lesson or day title
                subject_title = student_schedule.row_values(i)[1]
                group_title = student_schedule.row_values(i)[2]
                teacher_name = student_schedule.row_values(i)[3]
                cabinet_number = student_schedule.row_values(i)[4]

                if len(first_column) in range(1, 3):
                    current_lesson = Lesson(
                        subject_title, group_title, teacher_name, cabinet_number)

                    if '8' in group_title or '9' in group_title:
                        current_lesson.bell = bells_8_9[int(first_column) - 1]
                    if '10' in group_title or '11' in group_title:
                        current_lesson.bell = bells_10_11[int(first_column) - 1]

                    if teacher_name not in self.__TEACHERS.keys():
                        # 8 - maximum of lessons county
                        self.__TEACHERS[teacher_name] = {
                            'Понедельник' : None,
                            'Вторник' : None,
                            'Среда' : None,
                            'Четверг' : None,
                            'Пятница' : None,
                            'Суббота' : None
                        }

                    if not self.__TEACHERS[teacher_name][day_title]:
                        self.__TEACHERS[teacher_name][day_title] = Day(
                            day_title)
                        self.__TEACHERS[teacher_name][day_title].schedule = [
                            Lesson() for i in range(10)]

                    self.__TEACHERS[teacher_name][day_title].schedule[int(
                        first_column) - 1] = current_lesson

                elif len(first_column) != 0:
                    day_title = first_column

    @property
    def name(self):
        self.__update()

        for teacher_name in self.__TEACHERS:
            if self._name in teacher_name:
                self._name = teacher_name
                self._schedule = self.__TEACHERS[self._name]

        return self._name

    @property
    def schedule(self):
        self.name
        will_delete = list()

        for day_title in self._schedule:
            day = self._schedule[day_title]

            if not day:
                will_delete.append(day_title)
                continue

            checker = False
            for i in range(len(day.schedule) - 1, 0, -1):
                lesson = day.schedule[i]

                if (lesson.title == 'Окно' and not checker):
                    day.schedule.remove(lesson)

                if (lesson.title != 'Окно'):
                    checker = True

        for day_title in will_delete:
            self._schedule.pop(day_title)

        return self._schedule

    def __str__(self):
        return self.__title__
