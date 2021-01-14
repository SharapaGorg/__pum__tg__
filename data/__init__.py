from data.LogPython import LogManager
import sys, os

if sys.platform == "win32":
    connect_sign = "\\"
else:
    connect_sign = "/"

try:
    import xlrd
except:
    if sys.platform == "win32":
        os.system(f"python data{connect_sign}deps.py")
    else:
        os.system(f"python3 data{connect_sign}deps.py")
        
    sys.exit(0)
        
identities, folder = dict(), f"data{connect_sign}assets"
        
""" Creating a list of Identities """ 
for grid in os.listdir(folder):
    
    FILE = folder + connect_sign + grid

    data = xlrd.open_workbook(FILE)
    
    for i in range(1, len(data.sheet_names())):
        sh1, count = data.sheet_by_index(i), 0
        
        temp_index = 6
        
        if i == 1:
            temp_index = 7
        
        for l in range(sh1.nrows):
            temp_ = sh1.row_values(l)[temp_index]

            if temp_ != '':
                identities[temp_] = i
   
days = ["Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
                
def select_id(id_ : str):
    
    shedule = list()
    code = {"Воскресенье" : "Unknown Identity"} 
    
    for elem in identities:
        if id_ in elem:
            id_ = elem
            code["Воскресенье"] = "OK"
            break
    
    if code["Воскресенье"] != "OK":
        return {"Воскресенье" : "Unknown Identity"} 
    else:
        FILE = f"data{connect_sign}assets{connect_sign}9.xlsx"
        
        data, index_ = xlrd.open_workbook(FILE), identities[id_]
        
        sh1 = data.sheet_by_index(index_)
    
        for i in range(sh1.nrows):
            res = sh1.row_values(i)[1]
            
            if res != '':
                shedule.append(res)
            
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

    return ishedule