import os, sys
from re import split

from data.config import settings
from data.LogPython import LogManager
from data.__init__ import select_id
from data.utils import find_students_with_facts, item_list

if sys.platform == "win32" : spliter = "\\"
else: spliter = "/"

try:
    from aiogram import Bot, types
    from aiogram.dispatcher import Dispatcher
    from aiogram.dispatcher.storage import FSMContext
    from aiogram.dispatcher.filters.state import State, StatesGroup
    from aiogram.contrib.fsm_storage.memory import MemoryStorage
    from aiogram.utils import executor
except:
    os.system(f"python3 data{spliter}deps.py")
        
    sys.exit(0)

SHEDULE_FILE = "data" + spliter + "SHEDULE_DATA.json"

bot = Bot(token = settings['TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())

class SheduleDataInput(StatesGroup):
    r = State()
    
class FindingLessonDataInput(StatesGroup):
    r = State()

@dp.message_handler(commands = ['start'])
async def procces_start_command(message : types.Message):
    await message.reply("Салам алейкум")

@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'start - greeting')

@dp.message_handler(commands = ['shedule'])
async def proccess_shedule_command(msg : types.Message):
    await bot.send_message(msg.chat.id,'Напишите, кто Вы, в формате Фамилия Имя Отчество')
    await SheduleDataInput.r.set()
    
@dp.message_handler(commands = ['find_victim'])
async def proccess_find_victim_command(msg : types.Message):
    await bot.send_message(msg.chat.id, "Напишите запрос в формате урок урок_по_счёту день_недели\nНапример:\nинфорМАтика 1 чеТвеРГ\nоКНо 2 втОрник")
    await FindingLessonDataInput.r.set()
    
@dp.message_handler(commands = ['item_list'])
async def items_list(msg : types.Message):
    data = item_list()
    res = str() 
    for elem in data:   
        res += ("-" + str(elem).lower() + "\n")
        
    await bot.send_message(msg.from_user.id, res)

@dp.message_handler(state = FindingLessonDataInput.r)
async def find_victim(msg : types.Message, state : FSMContext):
    r = msg.text
    data = r.split()
    
    result = str()
    
    try:
        student_list = find_students_with_facts(SHEDULE_FILE, data[0].lower(), data[1].lower(), data[2].lower())
        
        for member in student_list:
            result += ("- " + member + " \n")
        
        LogManager.info(f"{msg.from_user.full_name} called {sys._getframe().f_code.co_name} [{msg.text}]")
        
        await bot.send_message(msg.from_user.id, result)
        
    except Exception as ex:
        await bot.send_message(msg.from_user.id, ex)
    
    await state.finish()

@dp.message_handler(state = SheduleDataInput.r)
async def shedule(msg : types.Message, state : FSMContext):
    r = msg.text
    try:
        res = str()
        data = select_id(r)
        
        res += data.name + ":\n"
        
        for day in data.shedule:

            res += "\n" + day.name + ":\n"
            
            for elem in day.shedule:
                spacer, temp_cab = 0, ''
                
                if len(elem.cab) < 3:
                    temp_cab = "000"
                elif len(elem.cab) > 3:
                    spacer = 4
                
                try:
                    res += temp_cab + elem.cab + ' ' * (16 - len(elem.cab) - len(temp_cab) - spacer) + str(elem) + '\n'
                except:
                    pass
                
        LogManager.info(f"{msg.from_user.full_name} called {sys._getframe().f_code.co_name} [{msg.text}]")
                
        await bot.send_message(msg.from_user.id, res)
    except Exception as e: 
        await bot.send_message(msg.from_user.id, "Unknown Identity. Try again (bye)")   
        LogManager.error(e)
        
    await state.finish()
    
if __name__ == '__main__':
    LogManager.info("Success connected")
    executor.start_polling(dp, skip_updates = True)