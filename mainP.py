from func import create_user , id_creator, used_password
import PersonDetection as SO
import time
import os
import sys
import time
try:
    from aiogram import Bot, Dispatcher, executor, md, types
    import asyncio
    from threading import Thread, Event
    import threading
except Exception as e:
    print(e)
    os.system('pip install aiogram & pip install asyncio & pip install threading')
    sys.exit("Restart the script.")


token = ""
api = Bot(token = token, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(api)


g1 = threading.Thread(target=SO.PersonD, args=())

switch_index = 0


id_creator()
dicty = {}
whitedict = {}
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
    id = message.chat.id
    if id in dicty.keys():
        await message.reply(md.text(md.bold("Здраствуй, ", dicty.get(id))))
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
        await message.reply(md.bold("Error"))

@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    await message.reply(md.bold('Test'))

#with open("PersonHere.jpg", "rb") as photo:
            #await message.reply_photo(photo)

@dp.message_handler(commands=['switch'])
async def switch(message: types.Message):
    global switch_index
    if switch_index == 0:
        switch_index += 1
        await message.reply(md.bold("0"))
        g1.start()
        await message.reply_photo("PersonHere.jpg")
    else:
        switch_index -= 1
        await message.reply(md.bold("1"))
        python = sys.executable
        os.execl(python, python, * sys.argv)
    

@dp.message_handler(commands=['status'])
async def status(message: types.Message):   
    global switch_index
    if switch_index == 0:
        await message.reply(md.bol("Система видеонаблюдения выключена"))
    else:
        await message.reply(md.bol("Система видеонаблюдения включена"))
def logo():
    print("""
                                                  
                      `/dd+`                      
                    :yNMMMMNy:                    
                ./sNMMMMMMMMMMNs/.                
      ymmmmmmmNMMMMMMMMMMMMMMMMMMMMNmmmmmmmy      
      hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMh      
      hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMh      
      hMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMh      
      hMMMMMMMMMMMMMmyo+//+oymMMMMMMMMMMMMMh      
      hMMMMMMMMMNy/`          `/yMMMMMMMMMMh      
      hMMMMMMMNs`    .sdmmds.    `sMMMMMMMMh      
      hMMMMMMm.     /MMMMMMMM/     .mMMMMMMh      
      hMMMMMM.      hMds+MMMMh      .MMMMMMh      
      hMMMMMMd.     /MMMMMMMM/     .dMMMMMMh      
      hMMMMMMMNo`    .sdmmds.    `oNMMMMMMMh      
      sMMMMMMMMMNy:`          `:yNMMMMMMMMMs      
      -MMMMMMMMMMMMMdyo+//+oydMMMMMMMMMMMMM-      
       +MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM+       
        /NMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMN/        
         `sMMMMMMMMMMMMMMMMMMMMMMMMMMMMs`         
           `+dMMMMMMMMMMMMMMMMMMMMMMd+`           
              `:smMMMMMMMMMMMMMMms:`              
                  .+hNMMMMMMNh+.                  
                      :sdds:

 HouSec (Alpha v0.2.2)
 Made by MaKxex                                        
    """)
logo()
executor.start_polling(dp, skip_updates=True)