import xlrd, os
from __init__ import select_id, connect_sign
from LogPython import LogManager
    
identities, folder = dict(), f"assets"
        
""" Creating a list of Identities """ 

for grid in os.listdir(folder):

    FILE = folder + connect_sign + grid

    data = xlrd.open_workbook(FILE)

    for i in range(0, len(data.sheet_names()) - 1):
        sh1, count = data.sheet_by_index(i), 0
        
        temp_index = 6
        
        if i == 0:
            temp_index = 7
        
        for l in range(sh1.nrows):
            temp_ = sh1.row_values(l)[temp_index]

            if temp_ != '':
                if len(str(temp_).split()) == 3:
                    identities[temp_] = i
import json

with open("latest_shedule.json", "w", encoding = "utf-8") as wrote:
    border, counter = len(identities.keys()), 0
    wrote.write("[")
    for name in identities.keys():
        json.dump({name : select_id(name, debug = 1, custom_id = identities)}, wrote, ensure_ascii=False)
        
        LogManager.info(name)
        counter += 1
        
        if counter != border:
            wrote.write(",")
            
    wrote.write(']')    