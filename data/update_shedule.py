import xlrd, os
# from __init__ import select_id, connect_sign
from LogPython import LogManager
    
identities, folder = dict(), f"data\\assets"
connect_sign ="\\"
days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
    
""" Creating a list of Identities """ 

for grid in os.listdir(folder):

    FILE = folder + connect_sign + grid

    data = xlrd.open_workbook(FILE)

    for i in range(0, len(data.sheet_names())):
        
        try: sh1, count = data.sheet_by_index(i), 0
        except: sh1, count = data.sheet_by_index(0), 0
        
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
                    identities[temp_] = l
            except : pass

def select_id(id_ : str, **kwargs):
    
    shedule, handled_list = list(), list()
    code = {"Воскресенье" : "Unknown Identity"} 
    
    if kwargs['custom_id']:
        handled_list = kwargs['custom_id']
    else:
        handled_list = identities
    
    for elem in handled_list:
        try:
            if id_ in elem:
                id_ = elem
                code["Воскресенье"] = "OK"
                break
        except: pass
    
    if code["Воскресенье"] != "OK":
        raise Exception("UnknownIdentity")
    else:
        FILE = f"data{connect_sign}assets{connect_sign}9.xlsx"
        if kwargs['debug'] : 
            FILE = f"assets{connect_sign}9.xlsx"
        
        data, index_ = xlrd.open_workbook(FILE), handled_list[id_]
        
        try: 
            sh1, checker = data.sheet_by_index(index_), 0
        except: 
            sh1, checker = data.sheet_by_index(0), 0
    
        for i in range(sh1.nrows):
            res = sh1.row_values(i)[1]
            
            if checker == 10:
                checker = 0
            
            if res == "Предмет" or (checker != 10 and checker != 0):
                shedule.append(res)
                
                checker += 1
            
        return handle_shedule(shedule)
    
def handle_shedule(shedule_ : list):
    ishedule = dict()
    count = 0 
    
    for elem in shedule_:
        if elem == "Предмет":
            shedule_.insert(shedule_.index(elem), days[count])
            count += 1
                
            shedule_.remove(elem)
     
    for i in range(5):
        ishedule[days[i]] = []
            
    count = -1
    for elem in shedule_:
        if elem not in days:
            ishedule[days[count]].append(elem)
        else:
            count += 1
            
    for day in ishedule.keys():
        for lesson in ishedule[day]:
            if lesson == '':
                ishedule[day][ishedule[day].index(lesson)] = "Окно"

    return ishedule

import json

with open("../latest_shedule.json", "w", encoding = "utf-8") as wrote:
    border, counter = len(identities.keys()), 0
    wrote.write("[")
    for name in identities.keys():
        json.dump({name : select_id(name, debug = 0, custom_id = identities)}, wrote, ensure_ascii=False)
        
        LogManager.info(name)
        counter += 1
        
        if counter != border:
            wrote.write(",")
            
    wrote.write(']')    