import os, sys

from data.config import settings
from data import LogPython
from data.utils import StudentShedule

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
    await bot.send_message(msg.chat.id, "Напишите запрос в формате день_недели урок урок_по_счёту\nНапример:\nчеТвеРГ инфорМАтика 1\nвтОрник оКНо 2")
    await FindingLessonDataInput.r.set()

@dp.message_handler(state = SheduleDataInput.r)
async def shedule(msg : types.Message, state : FSMContext):
    r = msg.text
    try:
        data = StudentShedule(r)
        
        res = data.name + ":\n\nДень недели:\nВремя начала - кабинет Название\n\n"
        res += f'Количество окон --> `{data.window_checker}`\n'

        groups = set()

        for day in data.shedule:
            res += "\n" + day.title + ":\n" 

            for lesson in day.shedule:
                spacer, temp_cab = 0, ''
                
                if len(lesson.cab) < 3:
                    temp_cab = "000"
                elif len(lesson.cab) > 3:
                    spacer = 4

                try:
                    res += lesson.bell + " - " + temp_cab + lesson.cab + ' ' * (16 - len(lesson.cab) - len(temp_cab) - spacer) + str(lesson) + '\n'
                except:
                    pass

                groups.add(lesson.group)

        groups.remove('')
        groups = list(groups)

        res += '\nВаши группы:\n'

        for i in range(2, len(groups), 3):
            if (groups[i - 2]): res += (groups[i - 2] + ' ')
            if (groups[i - 1]): res += (groups[i - 1] + ' ')
            if (groups[i]): res += (groups[i])

            res += '\n'

        LogPython.info(f"{msg.from_user.full_name} called {sys._getframe().f_code.co_name} [{msg.text}]")
                
        await bot.send_message(msg.from_user.id, res, parse_mode = 'markdown')
    except Exception as e: 
        import traceback
        await bot.send_message(msg.from_user.id, "Unknown Identity. Try again (bye)")   
        LogPython.error(e)
        LogPython.error(traceback.format_exc())
        
    await state.finish()
    
if __name__ == '__main__':
    LogPython.info("Success connected")
    executor.start_polling(dp, skip_updates = True)