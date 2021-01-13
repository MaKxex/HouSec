from aiogram import Bot, Dispatcher, executor, md, types
import time
import os
import sampleOrigins as SO
import asyncio
from threading import Thread, Event
import threading
import sys
import time
from func import create_user

token = ""
api = Bot(token = token, parse_mode=types.ParseMode.MARKDOWN)
dp = Dispatcher(api)


g1 = threading.Thread(target=SO.PersonD, args=())
switch_index = 0
whitelist = open("whitelist.txt", "r", encoding="utf-8").read().split(" ")


@dp.message_handler(commands=['start'])
async def heya(message: types.Message):
    id = message.chat.id
    create_user(id)
    await message.reply(md.text(
                        md.bold("Привет, используйте команду /login чтобы зайти в систему"),
                        md.bold("Пример /login Login Password"),
                                sep="\n"))

@dp.message_handler(commands=['login'])
async def register(message: types.Message):
    Mtext = message.get_args()
    
    # Что-то
    
    try:
        await message.reply(md.bold(Mtext))

    except Exception as BadRequest:
        await message.reply(md.bold("Сообщение пустое"))

@dp.message_handler(commands=['test'])
async def test(message: types.Message):
    await message.reply(md.bold('Test'))

@dp.message_handler(commands=['switch'])
async def switch(message: types.Message):
    global switch_index
    if switch_index == 0:
        switch_index += 1
        await message.reply(md.bold("0"))
        g1.start()
    else:
        switch_index -= 1
        await message.reply(md.bold("1"))
        python = sys.executable
        os.execl(python, python, * sys.argv)
    

@dp.message_handler(commands=['status'])
async def status(message: types.Message):   
    global switch_index

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

 HouSec (Alpha v0.2)
 Made by MaKxex                                        
    """)
logo()
executor.start_polling(dp, skip_updates=True)