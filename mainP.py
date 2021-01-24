from func import create_user , id_file_creator, used_password
import PersonDetection as SO
import time
import os
import sys
import time
import shutil
try:
    from aiogram import Bot, Dispatcher, executor, md, types
    import asyncio
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    from threading import Thread, Event
    import threading
except Exception as e:
    print(e)
    os.system('pip install aiogram & pip install asyncio & pip install threading')
    sys.exit("Restart the script.")


token = "!TOKEN!"
api = Bot(token = token, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(api)
sch = AsyncIOScheduler()

g1 = threading.Thread(target=SO.PersonD, args=())
Thread_stop = threading.Event()

# -----------
switch_index = 0
# -----------
id_file_creator()
dicty = {}
whitedict = {}
# -----------

async def sendPhoto():
    global switch_index
    chat = int("Chat_ID")
    if switch_index == 1:
        if os.path.exists("./PersonHere.jpg"):
            with open("PersonHere.jpg", "rb") as photo:
                await api.send_photo(chat,photo)
            shutil.move("./PersonHere.jpg","./UsedPhoto/PersonHere.jpg")
        else:
            print("Ничего не нашел")
    else:
        pass


def WUpdater(): #Ty NeverCore
    with open("id.txt", encoding='utf-8') as f:
        for line in f:
            (key, val) = line.split(",") # Key is UserId, Val is UserName
            dicty[int(val)] = key
    with open("whitelist.txt", encoding='utf-8') as w:
        for line in w:
            (key, val) = line.split(",") # Key is Password, Val is  ID if exist
            whitedict[key] = val
    
WUpdater()
print(dicty)
print("----------")
print(whitedict)

@dp.message_handler(commands=['start'])
async def heya(message: types.Message):
    WUpdater()
    chat_id = message.chat.id
    if id in dicty.keys():
        await message.reply(md.text(md.bold("Здраствуй, ", dicty.get(chat_id))))
    else:
        await message.reply(md.text(
                            md.bold("Привет, используйте команду /login чтобы зайти в систему"),
                            md.bold("Пример /login Login Password Name"),
                                    sep="\n"))

@dp.message_handler(commands=['login'])
async def register(message: types.Message):
    WUpdater() 
    Mtext = message.get_args().split(" ") # Login Password UserName
    print(Mtext) 
    user_id = message.chat.id

    try:
        if not user_id in dicty.keys(): # if ID in ID's pool

            if len(Mtext) < 3:
                await message.reply(md.text(
                                    md.bold('Не хватает данных!'),
                                    md.text("Введите по примеру /login Login Password Name"),
                                    sep="\n"))

            else:
                logpass = Mtext[0] + " " + Mtext[1]
                if not whitedict.get(logpass) == "":
                    await message.reply(md.bold("Этот пароль уже использован"))

                else:
                    if logpass in whitedict.keys():
                        create_user(user_id, Mtext[2])
                        used_password(logpass, user_id)
                        await message.reply(md.text(
                                            md.bold("Авторизация прошла успешно"),
                                            md.text("Здравствуй, " + Mtext[2]),
                                            sep="\n"))

                    else:
                        await message.reply(md.bold("Не верный Логин или Пароль"))
        else:
            await message.reply(md.text(
                                md.bold("Вы уже прошли Авторизацию"),
                                md.text("Эта команда вам больше не понадобится"),
                                sep="\n"))
    except Exception as e:
        print(e)
        await message.reply(md.bold("Error in login"))

@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    await message.reply(md.bold('Test'))

@dp.message_handler(commands=['switch'])
async def switch(message: types.Message):
    user_id = message.chat.id 
    global switch_index

    if user_id in dicty.keys(): # if ID in ID's pool
        if switch_index == 0:
            switch_index += 1
            await message.reply(md.bold("Система видеонаблюдения включена"))
            g1.start()
            sch.start()

        else:
            switch_index -= 1
            await message.reply(md.bold("Система видеонаблюдения выключена"))
            #python = sys.executable
            #os.execl(python, python, * sys.argv)
    else:
        await message.reply(md.text(
                                md.bold("Вы не прошли Авторизацию"),
                                md.text("Используйте команду /login"),
                                sep="\n"))
        
@dp.message_handler(commands=['status'])
async def status(message: types.Message):   
    global switch_index
    if switch_index == 0:
        await message.reply(md.bold("Система видеонаблюдения выключена"))
    else:
        await message.reply(md.bold("Система видеонаблюдения включена"))

'''
@dp.message_handler(commands=['shutdown'])
async def shutdown(message: types.Message):
    sys.exit()
'''



sch.add_job(sendPhoto,"interval", seconds=2)
def logo():
    print("""


     ___         ___         ___         ___         ___         ___     
    /__/\       /  /\       /__/\       /  /\       /  /\       /  /\    
    \  \:\     /  /::\      \  \:\     /  /:/_     /  /:/_     /  /:/    
     \__\:\   /  /:/\:\      \  \:\   /  /:/ /\   /  /:/ /\   /  /:/     
 ___ /  /::\ /  /:/  \:\ ___  \  \:\ /  /:/ /::\ /  /:/ /:/_ /  /:/  ___ 
/__/\  /:/\:/__/:/ \__\:/__/\  \__\:/__/:/ /:/\:/__/:/ /:/ //__/:/  /  /\\
\  \:\/:/__\\\  \:\ /  /:\  \:\ /  /:\  \:\/:/ /:\  \:\/:/ /:\  \:\ /  /:/
 \  \::/     \  \:\  /:/ \  \:\  /:/ \  \::/ /:/ \  \::/ /:/ \  \:\  /:/ 
  \  \:\      \  \:\/:/   \  \:\/:/   \__\/ /:/   \  \:\/:/   \  \:\/:/  
   \  \:\      \  \::/     \  \::/      /__/:/     \  \::/     \  \::/   
    \__\/       \__\/       \__\/       \__\/       \__\/       \__\/    



 HouSec (Alpha v0.3)
 Made by MaKxex                                        
    """)
logo()
executor.start_polling(dp, skip_updates=True)