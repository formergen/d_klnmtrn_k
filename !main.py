from __future__ import annotations
import asyncio
import logging
from time import sleep
import os
import datetime
import random
import requests
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.exceptions import Throttled
from aiogram.types import chat
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from pydantic import Field
from admin_filter import MyFilter
from aiogram.types import ContentType, Message
from picsc import *
from picsd import *
from gifsc import *
from config import *
import db1
from texts import *
import random
from dimapa import * 
import time
import glob
global user_id
from api import TikTokAPI
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
owners1 = [1779353481]
admins = db1.get_admin()
print(db1.get_admin())
dp.filters_factory.bind(MyFilter)
last_time = {}
last_taim = {}
linstart = 0
TikTok = TikTokAPI(
    link='tiktok.com',
    regexp_key=r'"video":{"id":"(.*?)",.*?"downloadAddr":"(.*?)",.*?}',
    headers={
        "Referer": "https://www.tiktok.com/",
    }
)

async def commands_list_menu(dp):
        await dp.bot.set_my_commands([
            types.BotCommand("start", "Запустить бота."),
            types.BotCommand("help", "Вывести команды бота."),
            types.BotCommand("capt", "Захватить Московию."),
            types.BotCommand("jerk", "Подрочить."),
            types.BotCommand("cat", "Отправить картинку кота."),
            types.BotCommand("dog", "Отправить картинку собаки(Временно не работает)."),
            types.BotCommand("random", "Вывести число в заданном вами промежутке."),
            #types.BotCommand("monetka", "Орёл и Решка."),
            #types.BotCommand("adminlist", "Вывести список администрации бота.")
            ]
)
async def on_startup(dp):
    await commands_list_menu(dp)

     
@dp.message_handler(commands=['ex_capt'])
async def ex_capt_use(message: types.Message):
    yaloh = int(message.from_user.id)
    a = db1.get_excapt(yaloh)
    inline_kb1 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Использовать 🏳️Экс-Захват🏳️', callback_data=f'use_capt_{yaloh}')).add(InlineKeyboardButton('Использовать все 🏳️Экс-Захваты🏳️', callback_data=f'useall_capt_{yaloh}'))    

    if a == None:
        await message.reply('Недостаточно Ex-захватов')
    elif a <= 0:
        await message.reply('Недостаточно Ex-захватов')
    else:

        a-=1
        db1.items_ex_capt(yaloh, a)
        db1.towns(yaloh, (db1.get_towns(yaloh)+2))
  
        await message.answer(f'Вы успешно применили Спец-Операцию "🏳️Ex-Захват🏳️" На Вашем счету {db1.get_towns(yaloh)} захваченных городов!\nОсталось {db1.get_excapt(yaloh)} Ex-Захватов', reply_markup=inline_kb1)
    @dp.callback_query_handler(text=f"use_capt_{yaloh}")
    async def send_st(call: types.CallbackQuery):
        yaloh1 = int(call.from_user.id)
        print(yaloh)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            if db1.get_excapt(yaloh1) == None:
                await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            elif db1.get_excapt(yaloh1) <= 0:
                await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            else:

                db1.items_ex_capt(yaloh1, (db1.get_excapt(yaloh1)-1))
                db1.towns(yaloh1, (db1.get_towns(yaloh1)+2))
            
                await call.message.answer(f'Вы применили Спец-Операцию "🏳️Ex-Захват🏳️" На Вашем счету {db1.get_towns(yaloh1)} захваченных городов!\nОсталось {db1.get_excapt(yaloh1)} Ex-Захватов')
    @dp.callback_query_handler(text=f'useall_capt_{yaloh}')
    async def use_all_capt(call: types.CallbackQuery):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1: await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            a = db1.get_excapt(yaloh1)
            if db1.get_excapt(yaloh1) == None: await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            elif db1.get_excapt(yaloh1) <= 0: await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            else:
                
                
                print(db1.get_towns(yaloh)+(int(db1.get_excapt(yaloh1))*2))
                db1.towns(yaloh, (db1.get_towns(yaloh)+(int(db1.get_excapt(yaloh1))*2)))
                db1.items_ex_capt(yaloh, 0)
                await call.message.answer(f'Вы применили все "🏳️Ех-Захват🏳️". На Вашем счету {db1.get_towns(yaloh1)} захваченных городов!')

    

#@dp.message_handler(content_types=[ContentType.NEW_CHAT_MEMBERS])
#async def new_members_handler(message: Message):
#    new_member = message.new_chat_members[0]
#    await bot.send_message(message.chat.id, f'{new_member.mention}пр я тебя в бд занесу и будешь хуи сасат поняд*?!?!??!?!?!')
#    print(message)
@dp.callback_query_handler(text="button1")
async def send_st(call: types.CallbackQuery):
    await call.message.answer(call.from_user.id)
@dp.message_handler(commands='test')
async def tryjj(message: types.Message):
    print(message.reply_to_message.from_user.id.is_chat_admin())
@dp.message_handler(commands=['захват', 'capt'])
async def sdfiu1(message: types.Message):
    yaloh = int(message.from_user.id)
    inline_kb1 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Использовать 🏳️Экс-Захват🏳️', callback_data=f'use_capt_{yaloh}')).add(InlineKeyboardButton('Использовать все 🏳️Экс-Захваты🏳️', callback_data=f'useall_capt_{yaloh}'))    
    towns = db1.get_towns(message.from_user.id)
    if towns == None:
        db1.towns(message.from_user.id, 0)
        towns = db1.get_towns(message.from_user.id)
    if message.from_user.id in last_taim:
        if message.text == "/захват" or message.text == '/capt' or message.text == '/capt@Akkamm4nj_bot':
            if (time.time() - last_taim[message.from_user.id]) > 6000:
                if random.randint(1,5) == 5:
                    towns += 1
                    db1.towns(message.from_user.id, towns)
                    if random.randint(1,3) == 3:
                        if db1.get_excapt(yaloh) == None:
                                db1.items_ex_capt(yaloh, 1)
                        else:
                            db1.items_ex_capt(yaloh, (db1.get_excapt(yaloh) + 1))
                        inline_kb1 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Использовать 🏳️Экс-Захват🏳️', callback_data=f'use_capt_{yaloh}')).add(InlineKeyboardButton('Использовать все 🏳️Экс-Захваты🏳️', callback_data='useall_capt'))
                        if db1.get_money(yaloh)==None:
                            random_money = random.randint(1,10)
                            db1.money(yaloh, random_money)
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                        else:
                            random_money = random.randint(1,10)
                            db1.money(yaloh, (int(db1.get_money(yaloh))+random_money))
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                        await message.answer(f'Поздравляем, вы захватили 1 город! Сейчас у вас захвачено {towns} городов. Так же вы получили 1 Спец-Операцию "🏳️Экс-Захват🏳️"! На вашем счету {db1.get_excapt(yaloh)} Экс-Захватов.\nПриходите играть снова через 1 час 40 минут.', reply_markup=inline_kb1)

                    else:
                        if db1.get_money(yaloh)==None:
                            random_money = random.randint(1,10)
                            db1.money(yaloh, random_money)
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                        else:
                            random_money = random.randint(1,10)
                            db1.money(yaloh, (int(db1.get_money(yaloh))+random_money))
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                        await message.answer(f'Поздравляем, вы захватили 1 город! Сейчас у вас захвачено {towns} городов. Приходите играть снова через 1 час 40 минут.', reply_markup=inline_kb1)
                else:
                    await message.answer('Не повезло! Ну ничего страшного, Приходите играть снова через 1 час 40 минут.', reply_markup=inline_kb1)                    
                last_taim[message.from_user.id] = time.time()
            elif (time.time() - last_taim[message.from_user.id] < 6000):
                timeponsex = round(int(time.time() - last_taim[message.from_user.id]) / 60, 2)
                await message.reply(f'Поджди ещё {round(100 - timeponsex, 2)} минут до своего следующего захвата!')
                  
    else:
        if random.randint(1,5) == 5:
            towns += 1
            db1.towns(yaloh, towns)
            if random.randint(1,3) == 3:
                if db1.get_excapt(yaloh) == None:
                        db1.items_ex_capt(yaloh, 1)
                else:
                    db1.items_ex_capt(yaloh, (db1.get_excapt(yaloh) + 1))
                inline_kb1 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Использовать 🏳️Экс-Захват🏳️', callback_data=f'use_capt_{yaloh}')).add(InlineKeyboardButton('Использовать все 🏳️Экс-Захваты🏳️', callback_data=f'useall_capt_{yaloh}'))
                if db1.get_money(yaloh)==None:
                            random_money = random.randint(1,20)
                            db1.money(yaloh, random_money)
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                else:
                            random_money = random.randint(1,20)
                            db1.money(yaloh, (int(db1.get_money(yaloh))+random_money))
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                await message.answer(f'Поздравляем, вы захватили 1 город! Сейчас у вас захвачено {towns} городов. \nТак же вы получили 1 Спец-Операцию "🏳️Экс-Захват🏳️"! На вашем счету {db1.get_excapt(yaloh)} Экс-Захватов. \nПриходите играть снова через 1 час 40 минут.', reply_markup=inline_kb1)

            else:
                if db1.get_money(yaloh)==None:
                            random_money = random.randint(1,20)
                            db1.money(yaloh, random_money)
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                else:
                            random_money = random.randint(1,20)
                            db1.money(yaloh, (int(db1.get_money(yaloh))+random_money))
                            await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                await message.answer(f'Поздравляем, вы захватили 1 город! Сейчас у вас захвачено {towns} городов. Приходите играть снова через 1 час 40 минут.', reply_markup=inline_kb1)
        else:
            await message.answer('Не повезло! Ну ничего страшного, Приходите играть снова через 1 час 40 минут.', reply_markup=inline_kb1)
        last_taim[yaloh] = time.time()
    @dp.callback_query_handler(text=f"use_capt_{yaloh}")
    async def send_st(call: types.CallbackQuery):
        yaloh1 = int(call.from_user.id)
        print(yaloh)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            if db1.get_excapt(yaloh1) == None:
                await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            elif db1.get_excapt(yaloh1) <= 0:
                await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            else:

                db1.items_ex_capt(yaloh1, (db1.get_excapt(yaloh1)-1))
                db1.towns(yaloh1, (db1.get_towns(yaloh1)+2))
            
                await call.message.answer(f'Вы применили Спец-Операцию "🏳️Ex-Захват🏳️" На Вашем счету {db1.get_towns(yaloh1)} захваченных городов!\nОсталось {db1.get_excapt(yaloh1)} Ex-Захватов')
    @dp.callback_query_handler(text=f'useall_capt_{yaloh}')
    async def use_all_capt(call: types.CallbackQuery):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1: await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            a = db1.get_excapt(yaloh1)
            if db1.get_excapt(yaloh1) == None: await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            elif db1.get_excapt(yaloh1) <= 0: await bot.answer_callback_query(call.id, "Недостаточно Ex-захватов", show_alert=False)
            else:
                
                
                print(db1.get_towns(yaloh)+(int(db1.get_excapt(yaloh1))*2))
                db1.towns(yaloh, (db1.get_towns(yaloh)+(int(db1.get_excapt(yaloh1))*2)))
                db1.items_ex_capt(yaloh, 0)
                await call.message.answer(f'Вы применили все "🏳️Ех-Захват🏳️". На Вашем счету {db1.get_towns(yaloh1)} захваченных городов!')

@dp.message_handler(is_admin=True, commands=["бан", 'ban', 'kick', 'кик'], commands_prefix='!/')
async def kick(message: types.Message):
        if message.reply_to_message:
            try:
                await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
                await message.reply_to_message.reply(
                    f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a> Заблокирован',
                    parse_mode='HTML')
            except Exception as e:
                await message.answer(e)
        elif not message.reply_to_message:
            await message.reply('Команда должна быть ответом на сообщение!')


@dp.message_handler(is_admin=True, commands = "mute")
async def mute(message: types.Message):
    if True:
        try:
            await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=time.time()+600)
            await message.answer(f'Пользователю запрещено право писать. Решение было принято @{message.from_user.username}')
        except Exception as e:
            await message.answer(e)
    else:
        await message.reply("Ей, ей, ей. Ты походу что-то попутал. Тебе нельзя использовать эту команду ")


    
@dp.message_handler(is_admin=True, commands = "unmute")
async def unmute(message: types.Message):
    admins = db1.get_admin()
    try:
        name = message.reply_to_message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
        if True:
            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                           can_send_messages=True,
                                           can_send_media_messages=True,
                                           can_send_other_messages=True)
            await bot.send_message(message.chat.id, f'Пользователь размучен.')

    except Exception as e:
        await message.answer(e)
                        
@dp.message_handler(commands=["бан", 'ban', 'kick', 'кик'], commands_prefix='!/')
async def kick(message: types.Message):
    admins = db1.get_admin()
    if message.from_user.id in admins or message.from_user.id == 656301126:
        if message.reply_to_message:
            try:
                await message.bot.kick_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id)
                await message.reply_to_message.reply(
                    f'<a href="tg://user?id={message.reply_to_message.from_user.id}">{message.reply_to_message.from_user.first_name}</a> Заблокирован',
                    parse_mode='HTML')
            except Exception as e:
                await message.answer(e)
        elif not message.reply_to_message:
            await message.reply('Команда должна быть ответом на сообщение!')
    else:
        await message.reply('Ты не админ в боте')

@dp.message_handler(commands = "mute")
async def mute(message: types.Message):
    admins = db1.get_admin()
    if message.from_user.id in admins:
        try:
            await message.bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id, until_date=time.time()+600)
            await message.answer(f'Пользователю запрещено право писать. Решение было принято @{message.from_user.username}')
        except Exception as e:
            await message.answer(e)
    else:
        await message.reply("Ей, ей, ей. Ты походу что-то попутал. Тебе нельзя использовать эту команду ")


    
@dp.message_handler(commands = "unmute")
async def unmute(message: types.Message):
    admins = db1.get_admin()
    try:
        name = message.reply_to_message.from_user.full_name
        user_id = message.reply_to_message.from_user.id
        if message.from_user.id in admins or message.from_user.id == 656301126:

            await bot.restrict_chat_member(chat_id=message.chat.id, user_id=message.reply_to_message.from_user.id,
                                           can_send_messages=True,
                                           can_send_media_messages=True,
                                           can_send_other_messages=True)
            await bot.send_message(message.chat.id, f'разблокирован.')
        else:
            await message.reply('Ты не админ в боте')
    except Exception as e:
        print(e)
@dp.message_handler(commands=['capt_top'])
async def capt_top(message: types.Message):
        await message.answer(db1.get_capt_top(), parse_mode="HTML")


@dp.message_handler(commands=['chat_admins', 'admins_list'])
async def ponch(message: types.Message):
        yaloh = int(message.from_user.id)
        listofad = await bot.get_chat_administrators(message.chat.id)
        inline_kb_ad = InlineKeyboardMarkup(row_width=3)
        for i in range(len(listofad)):
                inline_kb_ad.add(InlineKeyboardButton(listofad[i]["user"]["first_name"], callback_data=f'admin_{listofad[i]["user"]["id"]}')) 
                @dp.callback_query_handler(text=f'admin_{listofad[i]["user"]["id"]}')
                async def suka(call: types.CallbackQuery):
                    print(call["data"])
                    musor, id_ad = call["data"].split('admin_', 1)
                    
                    for admins_ad in listofad:
                        if int(admins_ad["user"]["id"]) == int(id_ad):
                            await call.message.edit_text(text=f'''
Ник: <a href="tg://user?id={admins_ad["user"]["id"]}">{admins_ad["user"]["first_name"]}</a>
Юзернейм: @{admins_ad["user"]["username"]}
Должность(Если есть): {admins_ad["custom_title"]}
Права:

Статус: {admins_ad["status"]}
Анонимность: {admins_ad["is_anonymous"]}
Может управлять чатом: {admins_ad["can_manage_chat"]}
Может удалять сообщения: {admins_ad["can_delete_messages"]}
Может ограничивать пользователей: {admins_ad["can_restrict_members"]}
''', reply_markup=inline_kb_ad, parse_mode='HTML')
        inline_kb_ad.add(InlineKeyboardButton("Закрыть список", callback_data='close')) 
        await message.answer('Актуальный список администрации чата', reply_markup=inline_kb_ad)
        
        @dp.callback_query_handler(text='close')
        async def close(call: types.CallbackQuery):
            yaloh1 = int(call.from_user.id)
            if yaloh != yaloh1:
                await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
            else:
                await call.message.delete()


        

        
@dp.message_handler(commands=['дрочить', 'jerk'])
async def sdfiu(message: types.Message):
    global drochka1
    global drochka
    
    yaloh = int(message.from_user.id)
    inline_kb2 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Использовать 💊Дрочелин💊', callback_data=f'use_lin_{yaloh}')).add(InlineKeyboardButton('Использовать весь 💊Дрочелин💊', callback_data=f'useall_lin_{yaloh}'))
    drochka1 = db1.get_droch(yaloh)
    if drochka1 == None:
        db1.droch(yaloh, 1)
        await message.reply('Привет! Вижу, ты впервые подрочил. С этого момента начинаю счет твоих дрочек. Сейчас твой счёт - 1 дрочка, приходи через 10 минут за следующей дрочкой')
        db1.items(yaloh, 0)
        last_time[message.chat.id] = time.time()

    else:
        if message.from_user.id in last_time:
            if message.text == "/дрочить":
                droblin = db1.get_lin(yaloh)
                if droblin == None:
                        db1.items(yaloh, 0)

                if (time.time() - last_time[message.from_user.id]) > 600:

                    db1.droch(yaloh, (int(db1.get_droch(yaloh))+1))
                    await message.reply(f'Ты успешно подрочил. Твоё кол-во дрочек - {drochka1+1}, приходи через 10 минут за следующей дрочкой', reply_markup=inline_kb2)
                    if db1.get_money(yaloh)==None:
                        random_money = random.randint(1,20)
                        db1.money(yaloh, random_money)
                        await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                    else:
                        random_money = random.randint(1,20)
                        db1.money(yaloh, (int(db1.get_money(yaloh))+random_money))
                        await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
                    if droblin == None:
                            db1.items(yaloh, 0)
                    else:
                        droblin = int(db1.get_lin(yaloh))
                    if random.randint(1,100) == 45:
                        droblin+=1
                        db1.items(yaloh, (int(db1.get_lin(yaloh))+1))
                        inline_kb2 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Использовать 💊Дрочелин💊', callback_data=f'use_lin_{yaloh}')).add(InlineKeyboardButton('Использовать весь 💊Дрочелин💊', callback_data=f'useall_lin_{yaloh}'))
                        await message.reply('Поздравляем!\n\n Вы получили 💊Дрочелин💊! (1 Дрочелин = 15 дрочек)\n\nШанс его получение - 1 на 100!', reply_markup=inline_kb2) 
                        
                    db1.conn.commit()
                    last_time[message.from_user.id] = time.time()
                elif (time.time() - last_time[message.from_user.id]) < 600:
                    timeponsex = round(int(time.time() - last_time[message.from_user.id]) / 60, 2)
                    await message.reply(f'Подoжди ещё {10 - timeponsex} минут до своей следующей дрочки!', reply_markup=inline_kb2)
        else:
            droblin = db1.get_lin(yaloh)
            if droblin == None:
                db1.items(yaloh, 0)
            else:
                droblin = int(db1.get_lin(yaloh))
            last_time[message.from_user.id] = time.time()  
            db1.droch(yaloh, (int(db1.get_droch(yaloh))+1))
            await message.reply(f'Ты успешно подрочил. Твоё кол-во дрочек - {drochka1+1}, приходи через 10 минут за следующей дрочкой', reply_markup=inline_kb2)
            if db1.get_money(yaloh)==None:
                random_money = random.randint(1,20)
                db1.money(yaloh, random_money)
                await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
            else:
                random_money = random.randint(1,20)
                db1.money(yaloh, (int(db1.get_money(yaloh))+random_money))
                await message.reply(f'Вы получили {random_money} монет! У вас на счету {db1.get_money(yaloh)} монет')
            if random.randint(1,100) == 45:
                droblin+=1
                db1.items(yaloh, (int(db1.get_lin(yaloh))+1))
                inline_kb2 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Использовать 💊Дрочелин💊', callback_data=f'use_lin_{yaloh}')).add(InlineKeyboardButton('Использовать весь 💊Дрочелин💊', callback_data=f'useall_lin_{yaloh}'))
                await message.reply('Поздравляем!\n\n Вы получили 💊Дрочелин💊! (1 Дрочелин = 15 дрочек)\n\nШанс его получение - 1 на 100!', reply_markup=inline_kb2)
            db1.conn.commit()

    @dp.callback_query_handler(text=f"use_lin_{yaloh}")
    async def send_st(call: types.CallbackQuery):
        yaloh1 = int(call.from_user.id)
        print(yaloh)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            if db1.get_lin(yaloh1) == None:
                await bot.answer_callback_query(call.id, "Недостаточно 💊Дрочелина💊", show_alert=False)
            elif db1.get_lin(yaloh1) <= 0:
                await bot.answer_callback_query(call.id, "Недостаточно 💊Дрочелина💊", show_alert=False)
            else:
                drochka1 = db1.get_droch(yaloh)+15
                db1.items(yaloh1, (db1.get_lin(yaloh1)-1))
                db1.droch(yaloh, drochka1)
                droblin=db1.get_lin(yaloh)
                await call.message.answer(f'Вы успешно использовали 💊Дрочелин💊, ваше количество дрочек - {drochka1}, осталось {droblin} 💊Дрочелина💊')
    
    @dp.callback_query_handler(text=f'useall_lin_{yaloh}')
    async def use_all_capt(call: types.CallbackQuery):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1: await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            a = db1.get_excapt(yaloh1)
            if db1.get_lin(yaloh1) == None: await bot.answer_callback_query(call.id, "Недостаточно 💊Дрочелин💊", show_alert=False)
            elif db1.get_lin(yaloh1) <= 0: await bot.answer_callback_query(call.id, "Недостаточно 💊Дрочелин💊", show_alert=False)
            else:
                drochka1 = db1.get_droch(yaloh)+(db1.get_lin(yaloh) * 15)
                db1.items(yaloh1, 0)
                db1.droch(yaloh, drochka1)
                await call.message.answer(f'Вы успешно использовали 💊Дрочелин💊, ваше количество дрочек - {drochka1}')
                 
            

@dp.message_handler(commands=['дрочелин', 'drochelin'])
async def dsfdf(message: types.Message):

    yaloh = int(message.from_user.id)
    drochka1 = db1.get_droch(yaloh)
    droblin = db1.get_lin(yaloh)
    if droblin == None:
        droblin = 0
        db1.items(yaloh, droblin)
    else:
        droblin = int(db1.get_lin(yaloh))
    if droblin <= 0 or droblin == None :
        droblin = 0
        db1.items(yaloh, droblin)
        await message.reply('У вас недостаточно 💊Дрочелина💊!')
    else:
        drochka1+=15
        db1.droch(yaloh, drochka1)
        droblin -= 1
        db1.items(yaloh, droblin)
        
        await message.reply(f'Вы успешно использовали 💊Дрочелин💊, ваше количество дрочек - {drochka1}, осталось {droblin} 💊Дрочелина💊')

    
@dp.message_handler(commands=['adminadd', 'админ+'], is_reply=True)

async def adminadd(message: types.Message):
    global admins
    if message.from_user.id in admins or  message.from_user.id in owners1:
        try:
            yaloh = int(message.reply_to_message.from_user.id)
            db1.add_admin(yaloh)
            admins = db1.get_admin()
            print(admins)
            await message.reply(f'Юзер <a href="tg://user?id={yaloh}">{message.reply_to_message.from_user.first_name}</a> добавлен в список администрации бота. Приветсуем!', parse_mode='HTML')
        except Exception as e:
            await message.reply(f'Произошла ошибка!\n\n{e}\n\nОбратитесь к создателю бота для её исправления!')
    else:
        await message.reply('Ты не админ!')
@dp.message_handler(commands=['admindel', "админ-"], is_reply=True)
async def admindel(message: types.Message):

    if message.from_user.id in owners1:
        yaloh = int(message.reply_to_message.from_user.id)
        db1.remove_admin(yaloh)
        admins = db1.get_admin()
        print(admins)
        await message.reply(f'Юзер <a href="tg://user?id={yaloh}">{message.reply_to_message.from_user.first_name}</a> удален из списка администрации. Прощай!', parse_mode='HTML')
    else:
        await message.reply('Ты не админ!')
    
@dp.message_handler(commands=['adminlist'])
async def adminslist(message: types.Message):
    admins = db1.get_admin()
    global adminslistsyka
    global podschet
    podschet=1
    adminslistsyka = f'<a href="tg://user?id=1779353481">Bot Owner </a> \n'
    await message.reply(f' Юзером <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> был запрошен список администрации!\nОбрабатываю...\nОжидайте секунду', parse_mode='HTML')
    print(admins)
    for i in admins:
        adminslistsyka = adminslistsyka + f'<a href="tg://user?id={i}">Bot Admin №{podschet}</a> \n'
        podschet+=1
    print(adminslistsyka)
    await message.reply(f'{adminslistsyka}', parse_mode='HTML')

    
@dp.message_handler(commands=['evefriends'])
async def evadruz(message: types.Message):
    await message.reply(f'<a href="tg://user?id=5150102639">drug1 </a> \n<a href="tg://user?id=5381680181">drug2 </a>\n<a href="tg://user?id=1766675750">drug3 </a>\n<a href="tg://user?id=1741990829">drug4 </a>\n<a href="tg://user?id=1399447302">drug5 </a>\n<a href="tg://user?id=1480202753">drug6 </a>\nСписок друзей Евелины ноточки', parse_mode='HTML')
    print('Evelina drizya zapros!!!! | ', message.from_user.id)
    
    
@dp.message_handler(commands=["infa", 'инфа', 'info', 'инфо'], commands_prefix='!/')
async def infa(message: types.Message):
    if message.reply_to_message == None:
        
        await message.reply(f"""💗Ваш инфа {message.from_user.get_mention(as_html=True)}: 💗 
🆔ID:{message.from_user.id} 🆔
🔅Username: @{message.from_user.username} 🔅
🌀Имя: {message.from_user.first_name} | {message.from_user.last_name}🌀
🐛Всего дрочек: {db1.get_droch(message.from_user.id)}🐛
🏙Всего захвачено городов: {db1.get_towns(message.from_user.id)}🏙
""", parse_mode='HTML')
        db1.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    if message.reply_to_message:
        
        await message.reply(f"""💗 инфа {message.reply_to_message.from_user.get_mention(as_html=True)}: 💗 
🆔ID:{message.reply_to_message.from_user.id} 🆔
🔅Username: @{message.reply_to_message.from_user.username} 🔅🌀Имя
Имя: {message.reply_to_message.from_user.first_name} | {message.reply_to_message.from_user.last_name}🌀
🐛Всего дрочек: {db1.get_droch(message.reply_to_message.from_user.id)}🐛
🏙Всего захвачено городов: {db1.get_towns(message.reply_to_message.from_user.id)}🏙

Новости бота: https://t.me/asoqwer_bot
""", parse_mode='HTML')
        db1.add_user(message.reply_to_message.from_user.id, message.reply_to_message.from_user.username, message.reply_to_message.from_user.first_name, message.reply_to_message.from_user.last_name)


@dp.message_handler(commands='getwin')
async def win(message: types.Message):
    winners = db1.get_win()
    await message.answer(f'Выиграли: {winners}', parse_mode='HTML')


@dp.message_handler(commands=["repost", 'рассылка'], commands_prefix='!/')
async def repost(message: types.Message):
    admins = db1.get_admin()
    repost = message.get_args().split()[1:]
    ss = ' '.join(repost)
    aa = int(message.get_args().split()[0])
    if message.from_user.id in admins or message.from_user.id == 656301126:
        while aa > 0:
            if aa >= 100:
                await message.reply('нельзя столько')
                break
            else:
                aa -= 1
                await asyncio.sleep(0.6)
                await message.answer(ss)
    else:
        await message.reply('Вы не админ')


@dp.message_handler(commands=["alt_repost", 'альт_рассылка'], commands_prefix='!/')
async def repost1(message: types.Message):
    admins = db1.get_admin()
    repost1 = message.get_args().split()[1:]
    ss1 = ' '.join(repost1)
    aa1 = int(message.get_args().split()[0])
    if message.from_user.id in admins or message.from_user.id == 656301126:
        if aa1 <= 20:
            await message.reply('Слишком маленький промежуток!')
        else:
            while True:
                sleep(aa1)
                await message.answer(ss1)
    else:
        await message.reply('Вы не админ')

@dp.message_handler(commands=['dimapic', 'димакартинка'])
async def picdima(message:types.Message):
    dimapap = random.randint(1,2)
    if dimapap == 1:
        await bot.send_sticker(chat_id=message.chat.id, sticker=random.choice(dimap))
    else:
        await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile(random.choice(dimapi)))
  

@dp.message_handler(commands=['cat', 'кот'])
async def cat_pic(message:types.Message):
    try:
        await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile(random.choice(catpic)))
        print(message.from_user.username, '|', message.from_user.id)
    except:
        await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile(random.choice(catpic)))
    
@dp.message_handler(commands=['catgif', 'котгиф'])
async def cat_pic(message:types.Message):
    await bot.send_animation(chat_id=message.chat.id, animation=types.InputFile(random.choice(catgif)))
                              
@dp.message_handler(commands=['dog', 'собака'])
async def cat_pic(message:types.Message):
    await message.answer('Временно не работает')
    #await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile(random.choice(dogpic)))


@dp.message_handler(commands=['random'])
async def send_cum(message: types.Message):
    repost = message.get_args().split()[1:]
    ss = ' '.join(repost)
    ss = int(ss)
    aa = int(message.get_args().split()[0])

    await message.reply(f'<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> Получил число - {random.randint(aa, ss)}', parse_mode='HTML')

@dp.message_handler(commands='send_m')
async def send_cum(message: types.Message):
    repost = message.get_args().split()[1:]
    ss = ' '.join(repost)
    aa = message.get_args().split()[0]
    await bot.send_message(aa, f'@{message.from_user.username} (user_id = {message.from_user.id}) |  сказал: {ss} \n\nЧто бы сделать так же - отправьте боту в лс /send_m {aa} сообщение')

@dp.message_handler(commands="start", commands_prefix='!/')
async def start(message: types.Message):
    await message.answer(
        f'Привет, <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>! Напиши /help,чтобы узнать что я умею\n\nНовости бота: https://t.me/asoqwer_bot',
        parse_mode="HTML")
    db1.add_user(user_id=message.from_user.id, username=message.from_user.username, name=message.from_user.first_name, last_name=message.from_user.last_name)



@dp.message_handler(commands=["хелп", 'help'], commands_prefix='!/')
async def help(message: types.Message):
    await message.reply(help_text)
    db1.add_user(user_id=message.from_user.id, username=message.from_user.username, name=message.from_user.first_name, last_name=message.from_user.last_name)
dhhsdhjfhsjdfsjhdfsdhj = r'''
@dp.message_handler()
async def da_net(message: types.Message):
    admins = db1.get_admin()
    if message.from_user.id in admins or message.from_user.id == 656301126:
        pass
    else:
        for texts in da:
            if texts == message.text:
                a=random.randint(1, 2)
                if a == 1:
                    await message.reply('пизда👎🏿')
                else:
                    await message.reply('Согл🙄')
        for net_text in net:
            if net_text == message.text:
                a=random.randint(1, 2)
                if a == 1:
                    await message.reply('пидора ответ👎🏿')
                else:
                    await message.reply('Согл🙄')
        for pohui_dima in pohui:
            if pohui_dima in message.text:
                await message.reply('Пошёл нахуй😡')
        for nea_bl in nea:
            if nea_bl in message.text:
                await message.reply('че неа, да как бы')
        for dima in dimacraah:
            if dima in message.text:
                await message.reply('Краш😈!') 
                await bot.send_sticker(chat_id=message.chat.id, sticker=r'CAACAgIAAxkBAAEEnB9ib7TztAgfhmMEptRA0hFeAxEFdQACWBAAArchIEg5pyzYcG_UkSQE')
        for idinahui in nahui:
            if idinahui in message.text:
                await message.reply("Сам нахуй иди😭!! ") 
        for anya in anna:
            if anya in message.text:
                await bot.send_photo(chat_id=message.chat.id, photo=types.InputFile(r'C:\Users\1\Documents/1.jpg'))
                
@dp.message_handler(commands=['money'])
async def monetka(message:types.Message):
    monetkaroll = random.randint(1,2)
    if monetkaroll == 1:
        await message.reply("Орёл!")
    else:
        await message.reply("Решка!")
      
@dp.message_handler(is_reply=True)
async def da_nets(message: types.Message):
    if message.from_user.id in admins or message.from_user.id == 656301126:
        pass
    else:
        for texts in da:
            if texts == message.text:
                a=random.randint(1, 2)
                if a == 1:
                    await message.reply('пизда👎🏿')
                else:
                    await message.reply('Согл🙄')
        for net_text in net:
            if net_text == message.text:
                a=random.randint(1, 2)
                if a == 1:
                    await message.reply('пидора ответ👎🏿')
                else:
                    await message.reply('Согл🙄')
        for pohui_dima in pohui:
            if pohui_dima in message.text:
                await message.reply('Пошёл нахуй😡')
        for nea_bl in nea:
            if nea_bl in message.text:
                await message.reply('че неа, да как бы')
        for dima in dimacraah:
            if dima in message.text:
                await message.reply('Краш😈!') 
        for idinahui in nahui:
            if idinahui in message.text:
                await message.reply("Сам нахуй иди😭!! ") 
        for anya in anna:
            if anya in message.text:
                await bot.send_photo(chat_id=message.chat.id, photo=photo)

'''
class Mydialog(StatesGroup):
    otvet = State()
class Mydialog1(StatesGroup):
    otvet1 = State()
@dp.message_handler(commands='market')
async def but1test(message: types.Message):
    global yaloh
    global yaloh1
    print(message)
    yaloh=message.from_user.id
    inline_kb_market = InlineKeyboardMarkup(row_width=3)
    inline_kb_market.add(InlineKeyboardButton('Дрочелин', callback_data='drolin')).add(InlineKeyboardButton('Экс-Захват', callback_data='captex')).add(InlineKeyboardButton('Закрыть маркет.', callback_data='close'))
    await message.reply(market_text, reply_markup=inline_kb_market)
    @dp.callback_query_handler(text=f"drolin", state = '*')
    async def send_st(call: types.CallbackQuery, state=Mydialog.otvet):
        await state.finish()
        yaloh1 = int(call.from_user.id)
        print(yaloh)
        print(yaloh1)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Покупка более 1 шт.', callback_data='ord_buy_d')).add(InlineKeyboardButton('Купить 1 шт. Дрочелина', callback_data='buy_drolin')).add(InlineKeyboardButton('Покупка Экс-Захвата', callback_data='captex')).add(InlineKeyboardButton('Закрыть маркет', callback_data='close'))
            await call.message.edit_text(market_droblin, reply_markup=inline_kb_market)

    @dp.callback_query_handler(text=f"captex", state = '*')
    async def send_st2(call: types.CallbackQuery, state=Mydialog.otvet):
        await state.finish()
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Покупка более 1 шт.', callback_data='ord_buy_c')).add(InlineKeyboardButton('Купить 1 шт. Экс-Захвата', callback_data='buy_capt')).add(InlineKeyboardButton('Покупка Дрочелина', callback_data='drolin')).add(InlineKeyboardButton('Закрыть маркет', callback_data='close'))
            await call.message.edit_text(market_capt, reply_markup=inline_kb_market)
    @dp.callback_query_handler(text='ord_buy_c')
    async def ord_buy_c(call: types.CallbackQuery, state: FSMContext):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Отменить заказ', callback_data='captex', state='*'))
            await call.message.edit_text(text='Напишите желаемое кол-во Экс-Захватов', reply_markup=inline_kb_market)
            await Mydialog.otvet.set()
            @dp.message_handler(state=Mydialog.otvet)
            async def process_messagea(message: types.Message, state: FSMContext):
                inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Отменить заказ?', callback_data='captex', state='*'))
                async with state.proxy() as data1:
                    data1['text']=message.text
                    user_message = data1['text']
                            
                    while str(user_message).isdigit() != True:
                        await call.message.edit_text(text='Введите число, а не строку!', reply_markup=inline_kb_market)
                    if int(db1.get_money(yaloh)) >= int(user_message)*20:
                        db1.money(yaloh, (int(db1.get_money(yaloh)-(int(user_message)*20))))
                        db1.items_ex_capt(yaloh, (int(db1.get_excapt(yaloh))+int(user_message)))
                        await message.reply(f'У вас осталось {db1.get_money(yaloh)} монет. \n\nЭкс-Захватов в Вашем инвентаре: {db1.get_excapt(yaloh)}')
                    else:
                        await message.reply(f'Вам не хватает {(int(user_message)*20)-(db1.get_money(yaloh))} монет.')
                inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Да.', callback_data='captex')).add(InlineKeyboardButton('Нет', callback_data='close'))
                await state.finish()
                await message.answer("Желаете купить ещё что то?", reply_markup=inline_kb_market)
    @dp.callback_query_handler(text='buy_capt')
    async def buy_c(call: types.CallbackQuery, state: FSMContext):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            if int(db1.get_money(yaloh)) >= 20:
                db1.money(yaloh, (int(db1.get_money(yaloh)-20)))
                db1.items_ex_capt(yaloh, (int(db1.get_excapt(yaloh))+1))
                await bot.answer_callback_query(call.id, f"Вы успешно купили 1 шт. Экс-Захват! У вас осталось {db1.get_money(yaloh)} монет.", show_alert=False)

            else:
                await bot.answer_callback_query(call.id, f'Вам не хватает {20-(db1.get_money(yaloh))} монет.', show_alert=False)
            inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Да.', callback_data='captex')).add(InlineKeyboardButton('Нет', callback_data='close'))
            await call.message.edit_text("Желаете купить ещё что то?", reply_markup=inline_kb_market)
    @dp.callback_query_handler(text='ord_buy_d')
    async def ord_buy_d(call: types.CallbackQuery, state: FSMContext):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Отменить заказ', callback_data='drolin', state = '*'))
            await call.message.edit_text(text='Напишите желаемое кол-во Дрочелин', reply_markup=inline_kb_market)
            await Mydialog1.otvet1.set()
            @dp.message_handler(state=Mydialog1.otvet1)
            async def process_message(message: types.Message, state: FSMContext):
                inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Отменить заказ?', callback_data='captex', state='*'))
                async with state.proxy() as data:
                    data['text']=message.text
                    user_message = data['text']
                    while str(user_message).isdigit() != True:
                        try:
                            await call.message.edit_text(text='Введите число, а не строку!', reply_markup=inline_kb_market)
                        except:
                            pass
                    if int(db1.get_money(yaloh)) >= int(user_message)*100:
                        db1.money(yaloh, (int(db1.get_money(yaloh)-(int(user_message)*100))))
                        db1.items(yaloh, (int(db1.get_lin(yaloh))+int(user_message)))
                        await message.answer(f'У вас осталось {db1.get_money(yaloh)} монет. \n\nДрочелина в Вашем инвентаре: {db1.get_lin(yaloh)}')
                    else:
                        await message.answer(f'Вам не хватает {(int(user_message)*100)-(db1.get_money(yaloh))} монет.')
                    await state.finish()
                inline_kb_market1 = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Да.', callback_data='drolin')).add(InlineKeyboardButton('Нет', callback_data='close'))    
                await message.answer("Желаете купить ещё что то?", reply_markup=inline_kb_market1)

    @dp.callback_query_handler(text='buy_drolin')
    async def buy_d(call: types.CallbackQuery, state: FSMContext):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            if int(db1.get_money(yaloh)) >= 100:
                db1.money(yaloh, (int(db1.get_money(yaloh)-100)))
                db1.items(yaloh, (int(db1.get_lin(yaloh))+1))
                await bot.answer_callback_query(call.id, f"Вы успешно купили 1 шт. Дрочелина! У вас осталось {db1.get_money(yaloh)} монет.", show_alert=False)

            else:
                await bot.answer_callback_query(call.id, f'Вам не хватает {100-(db1.get_money(yaloh))} монет.', show_alert=False)
            inline_kb_market = InlineKeyboardMarkup(row_width=3).add(InlineKeyboardButton('Да.', callback_data='drolin')).add(InlineKeyboardButton('Нет', callback_data='close'))
            await call.message.edit_text("Желаете купить ещё что то?", reply_markup=inline_kb_market)                


    @dp.callback_query_handler(text='close')
    async def close(call: types.CallbackQuery):
        yaloh1 = int(call.from_user.id)
        if yaloh != yaloh1:
            await bot.answer_callback_query(call.id, "Эта кнопка не для тебя", show_alert=False)
        else:
            await call.message.delete()

@dp.message_handler(commands=['monetka', 'money', 'монетка'])
async def monetka(message: types.Message):               
        monetkaroll = random.randint(1,2)
        chislo = message.get_args()
        if chislo == '' or chislo == ' ' or chislo == None:
                await message.reply('Введены неправильные параметры. Пример: /monetka 1')
        elif int(chislo) != 1 and int(chislo) != 2:
                await message.reply('Введены неправильные параметры. Пример: /monetka 1')
        else:       
                if monetkaroll == int(chislo):
                        await message.reply('Вы выиграли!')
                else:
                        if monetkaroll == 1:
                                await message.reply('Вы проиграли, выпал Орёл.')
                        else:
                                await message.reply('Вы проиграли, выпала Решка.')
                                
@dp.message_handler(commands='monetka_help')
async def monetkahelp(message: types.Message):
    await message.answer('Для использования этой команды нужно написать число после команды. 1 - Орёл, 2 - Решка. \n\nПример: /монетка 2')

@dp.message_handler()
async def da_nets(message: types.Message):
        if os.path.exists(f'messages/{message.chat["id"]}_{message.chat["title"]}.html') == True or os.path.exists(f'messages/{message.chat["id"]}.html') == True:
                try:
                    
                    dt_str6 = '{:%d/%m/%y %I:%M %S}'.format(datetime.datetime.today())
                    a = open(f'messages/{message.chat["id"]}_{message.chat["title"]}.html', 'a', encoding='utf-8', errors='ignore').write(f'''

     <div class="message default clearfix" id="message483039">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic1" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
{message["from"]["first_name"][0]}
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="08.07.2022 17:57:41 UTC+02:00">
{dt_str6}
       </div>

       <div class="from_name">
{message["from"]["first_name"]} 
       </div>

       <div class="text">
{message.text}
       </div>

      </div>

     </div>
''')
                except:
                        dt_str6 = '{:%d/%m/%y %I:%M %S}'.format(datetime.datetime.today())
                        a = open(f'messages/{message.chat["id"]}.html', 'a', encoding='utf-8', errors='ignore').write(f'''

     <div class="message default clearfix" id="message483039">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic1" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
{message["from"]["first_name"][0]}
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="08.07.2022 17:57:41 UTC+02:00">
{dt_str6}
       </div>

       <div class="from_name">
{message["from"]["first_name"]} 
       </div>

       <div class="text">
{message.text}
       </div>

      </div>

     </div>
''')                            
        else:
                try:
                    dt_str6 = '{:%d/%m/%y %I:%M %S}'.format(datetime.datetime.today())
                    a = open(f'messages/{message.chat["id"]}_{message.chat["title"]}.html', 'a', encoding='utf-8', errors='ignore').write(f'''
<!DOCTYPE html>
<html>

 <head>

  <meta charset="utf-8"/>
<title>Exported Data</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>

  <link href="css/style.css" rel="stylesheet"/>

  <script src="js/script.js" type="text/javascript">

  </script>

 </head>

 <body onload="CheckLocation();">

  <div class="page_wrap">

   <div class="page_header">

    <div class="content">

     <div class="text bold">
{message.chat["title"]}
     </div>

    </div>

   </div>

   <div class="page_body chat_page">

    <div class="history">

     <div class="message service" id="message-1">

      <div class="body details">
{dt_str6}
      </div>

     </div>

     <div class="message default clearfix" id="message483038">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic2" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
{message["from"]["first_name"][0]}
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="{dt_str6} UTC+02:00">
{dt_str6}
       </div>

       <div class="from_name">
{message["from"]["first_name"]} 
       </div>

       <div class="text">

{message.text}
       </div>

      </div>

     </div>

''')
                except:
                    dt_str6 = '{:%d/%m/%y %I:%M %S}'.format(datetime.datetime.today())
                    a = open(f'messages/{message.chat["id"]}.html', 'a', encoding='utf-8', errors='ignore').write(f'''
<!DOCTYPE html>
<html>

 <head>

  <meta charset="utf-8"/>
<title>Exported Data</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>

  <link href="css/style.css" rel="stylesheet"/>

  <script src="js/script.js" type="text/javascript">

  </script>

 </head>

 <body onload="CheckLocation();">

  <div class="page_wrap">

   <div class="page_header">

    <div class="content">

     <div class="text bold">
{message.chat["title"]}
     </div>

    </div>

   </div>

   <div class="page_body chat_page">

    <div class="history">

     <div class="message service" id="message-1">

      <div class="body details">
{dt_str6}
      </div>

     </div>

     <div class="message default clearfix" id="message483038">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic2" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
{message["from"]["first_name"][0]}
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="{dt_str6} UTC+02:00">
{dt_str6}
       </div>

       <div class="from_name">
{message["from"]["first_name"]} 
       </div>

       <div class="text">

{message.text}
       </div>

      </div>

     </div>

''')




   
if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
    commands_list_menu(dp)
