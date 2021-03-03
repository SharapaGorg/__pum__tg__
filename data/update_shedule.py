import sys, xlrd

students = dict() # identity : ( course, index_of_excel_table )

if sys.platform == "win32" : spliter = "\\"
else: spliter = "/"

if __name__ == "__main__":
    folder = "assets" + spliter
else:
    folder = "data" + spliter + "assets" + spliter

def is_indentity( name_object : str ) -> bool:
    return name_object != '' and len(name_object.split()) == 3
    

def filler( course : int, active : int, unusual_positions : dict, *pass_index):
    """
    
    course - school course of education of student
    active - active rows in every excel_index
    pass_index - excel_index without student`s names 
    unusual_positions - ( <excel_index , that has some changes> , <new_active_row> )
    
    P.S : active_rows - rows in every excel_index, that have student`s names
    
    """
    
    SOURCE = folder + str(course) + ".xlsx"
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
                    students[identity] = (_course, index_of_excel_table)
                    
            except: pass
            
filler(8, 7, {5 : 6} , 0) # fill 8s course
