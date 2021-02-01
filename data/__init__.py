import sys, os

if sys.platform == "win32":
    connect_sign = "\\"
else:
    connect_sign = "/"
    
try:
    import xlrd
except:
    if sys.platform == "win32":
        os.system(f"python deps.py")
    else:
        os.system(f"python3 data{connect_sign}deps.py")
        
    sys.exit(0)

try:
    from data.LogPython import LogManager
            
    identities, folder = dict(), f"data{connect_sign}assets"
            
    """ Creating a list of Identities """ 

    for grid in os.listdir(folder):

        FILE = folder + connect_sign + grid

        data = xlrd.open_workbook(FILE)

        for i in range(0, len(data.sheet_names())):
            sh1, count = data.sheet_by_index(i), 0
            
            temp_index = 6
            
            if i == 0:
                temp_index = 7
            
            for l in range(sh1.nrows):
                temp_ = sh1.row_values(l)[temp_index]

                if temp_ != '':
                    identities[temp_] = i
except:
    from LogPython import LogManager
    LogManager.warning("You shouldn`t run imported util")
      
days = ["Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
                
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
        
        sh1, checker = data.sheet_by_index(index_), 0
    
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

def item_list():
    res = set()
    
    with open(f"data{connect_sign}latest_shedule.json", "r", encoding = "utf-8") as handled:
        data = json.loads(handled.readline())
        res = set()
        
        for member in data:
            for day in member.values():
                for item_kit in day.values():
                    for item in item_kit:  
                        res.add(item.upper())
                        
    return res