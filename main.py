import os, sys

from aiogram.types import user
from data import LogPython

from data.config import settings
from data.LogPython import LogManager
from data.__init__ import select_id

try:
    from aiogram import Bot, types
    from aiogram.dispatcher import Dispatcher
    from aiogram.dispatcher.storage import FSMContext
    from aiogram.dispatcher.filters.state import State, StatesGroup
    from aiogram.contrib.fsm_storage.memory import MemoryStorage
    from aiogram.utils import executor
except ImportError as e:
    if sys.platform == "win32":
        os.system("python data\deps.py")        
    else:
        os.system("python data/deps.py")
        
    sys.exit(0)

bot = Bot(token = settings['TOKEN'])
dp = Dispatcher(bot, storage=MemoryStorage())

class DataInput(StatesGroup):
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
    await DataInput.r.set()

@dp.message_handler(state = DataInput.r)
async def shedule(msg : types.Message, state : FSMContext):
    r = msg.text
    _shedule_ = select_id(r)
    
    res = str()
    
    for elem in _shedule_.keys():
        res += elem + ': \n'

        for i in _shedule_[elem]:
            res += "- " + i + "\n"
            
    LogManager.info(f"{msg.from_user.full_name} called {sys._getframe().f_code.co_name}")
            
    await bot.send_message(msg.from_user.id, res)
    await state.finish()

# @dp.message_handler()
# async def echo_message(msg: types.Message):
#     await bot.send_message(msg.from_user.id, msg.text)
    
if __name__ == '__main__':
    LogManager.info("Success connected")
    executor.start_polling(dp, skip_updates = True)