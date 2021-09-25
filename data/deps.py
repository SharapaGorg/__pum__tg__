import os, sys

def deps_loader(command):
    os.system(
        'cd \"' + os.path.dirname(sys.executable) + '\" && ' + os.path.basename(sys.executable) + ' -m ' + command
    )
    
deps_loader("pip install aiogram requests click xlrd==1.2.0")