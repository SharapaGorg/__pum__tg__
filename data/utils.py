import xlrd

class Member:
    def __init__(self, name, year, excel_index):
        self.name = name
        self.year = str(year) + ".xlsx"
        self.excel_index = excel_index
        self.shedule = list()
        
    def push_day(self, day):
        self.shedule.append(day)
        
    def push_shedule(self, _):
        self.shedule = _
        
    def __str__(self) -> str:
        return self.name[0] + self.name[1:]
        
class Day:
    def __init__(self, name):
        self.name = name
        self.shedule = list()
        
    def push_lesson(self, lesson):
        self.shedule.append(lesson)
        
    def __str__(self) -> str:
        return self.name[0] + self.name[1:]
    
class Lesson:
    def __init__(self, name, group : str, cab : str, teacher : str):
        try:
            self.cab = str(int(float(cab)))
        except:
            self.cab = cab
            
        self.name = name
        self.group = group
        self.teacher = teacher
        
    def __str__(self) -> str:
        try:
            return self.name[0].upper() + self.name[1:]
        except:
            raise Exception("-")

def is_indentity( name_object : str ) -> bool:
    return name_object != '' and len(name_object.split()) == 3

def capital_reg(word : str) -> str:
    return word[0].upper() + word[1:]

def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k

def filler( source : str, members : list, course : int, active : int, unusual_positions : dict, *pass_index):
    """
    
    course - school course of education of student
    active - active rows in every excel_index
    pass_index - excel_index without student`s names 
    unusual_positions - ( <excel_index , that has some changes> , <new_active_row> )
    
    P.S : active_rows - rows in every excel_index, that have student`s names
    
    """
    
    SOURCE = source + str(course) + ".xlsx"
    data = xlrd.open_workbook(SOURCE)
    pass_index = list(pass_index)
    
    for i in range(0, len(data.sheet_names())):
        sh1, temp_active, accept_handling = data.sheet_by_index(i), active, 1
        
        for k in range(len(pass_index)): # checking for junk excel_index list
            if pass_index[k] == i:
                accept_handling = 0
                pass_index.remove(pass_index[k])
                break
         
        if not accept_handling: 
            continue
        
        for elem in unusual_positions: # checking for unusual changes in course.xlsx
            if i == elem:
                temp_active = unusual_positions[elem]
        
        for j in range(sh1.nrows):
            try:
                identity = sh1.row_values(j)[temp_active]
                _course = course
                index_of_excel_table = i
                
                if is_indentity (identity): # checking for correctly writing
                    members.append(Member(identity, _course, index_of_excel_table))
                    
            except: pass