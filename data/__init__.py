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