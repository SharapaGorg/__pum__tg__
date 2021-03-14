import sys
# from data.utils import filler
# from data.utils import return_static_shedule

from utils import filler, return_static_shedule

students = list() # Member(identity, _course, index_of_excel_table) * len(students)

if sys.platform == "win32" : spliter = "\\"
else: spliter = "/"

if __name__ == "__main__":
    folder = "assets" + spliter
else:
    folder = "data" + spliter + "assets" + spliter
    
# ------------ BODY ------------ #

filler(folder, students, 8, 7, {5 : 6} , 0)         
filler(folder, students, 9, 6, {0 : 7}, 24)        
filler(folder, students, 10, 6, {}, 9)              
filler(folder, students, 11, 6, {9 : 7, 11 : 7}, 0)

data = return_static_shedule(students, folder)