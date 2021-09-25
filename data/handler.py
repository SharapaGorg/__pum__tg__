import click
import LogPython
import sys
import xlrd
import os
from constants import static_folder, assets_folder
from utils import Lesson, Day

# TEACHERS = {
#    TEACHER_NAME : [class_name_at_first_lesson, class_name_at_second_lesson, ...],
#    ...
# }

TEACHERS = {}

if sys.platform == "win32":
    spliter = "\\"
else:
    spliter = "/"


class Student:
    __title__ = 'Teacher'
    __folder__ = static_folder + spliter + __title__ + '.json'

    def __init__(self, *args):
        self.args = args

    def update(self):
        return f'Successfully updated -> {self.__title__}.update'

    def __getattribute__(self, name: str):
        return super(Student, self).__getattribute__(name.lstrip('--'))

    def __str__(self):
        return self.__title__


class Teacher:
    __title__ = 'Teacher'
    __folder__ = static_folder + spliter + __title__ + '.json'

    def __init__(self, *args):
        self.args = args

    def update(self):
        """
        Update teacher`s schedule and fill with new information
        base on all students schedule
        """

        for student in os.listdir(assets_folder):
            student_schedule = xlrd.open_workbook(
                assets_folder + spliter + student).sheet_by_index(0)

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

                    if teacher_name not in TEACHERS.keys():
                        # 8 - maximum of lessons county
                        TEACHERS[teacher_name] = dict()

                    if day_title not in TEACHERS[teacher_name].keys():
                        TEACHERS[teacher_name][day_title] = Day(day_title)
                        TEACHERS[teacher_name][day_title].schedule = [
                            Lesson() for i in range(10)]

                    TEACHERS[teacher_name][day_title].schedule[int(
                        first_column) - 1] = current_lesson

                elif len(first_column) != 0:
                    day_title = first_column

            # break

        return f'Successfully updated -> {self.__title__}.update'

    def __getattribute__(self, name: str):
        return super(Teacher, self).__getattribute__(name.lstrip('--'))

    def __str__(self):
        return self.__title__


@click.command()
@click.option('-s', help='Student action : [--update]')
@click.option('-t', help='Teacher acion : [--update]')
def handler(s, t):
    method = str()

    try:
        if s:  # student action
            sample = Student()
            method = getattr(sample, s)()

        if t:  # teacher action
            sample = Teacher()
            method = getattr(sample, t)()

            for day in TEACHERS['Ляпин Н.А.']:
                print(day)

                for lesson in TEACHERS['Ляпин Н.А.'][day].schedule:
                    print(lesson, lesson.group, lesson.cab)

    except Exception as e:
        LogPython.warning('Invalid action (--help)')
        LogPython.error(e)
        import traceback
        LogPython.error(traceback.format_exc())

    LogPython.info(method)


if __name__ == '__main__':
    handler()
