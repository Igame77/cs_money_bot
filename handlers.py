from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters.callback_data import CallbackData
import config
import parser
from asyncio import sleep
from aiogram.utils.markdown import  hbold, hlink
from aiogram.enums.parse_mode import ParseMode

router = Router()

class ButtonAdd(CallbackData, prefix = 'any'):
    theme: str
    offset: int

@router.message(Command(commands = ['start']))
async def process_start_command(message : Message):
    buttons = [
        [KeyboardButton(text = '🔪Ножи🔪'),
        KeyboardButton(text = '🥊перчатки🥊'),
        KeyboardButton(text = '🎯Снайперские винтовки🎯'),
        KeyboardButton(text = '🔫пистолеты🔫')],
        [
            KeyboardButton(text = 'Штурмовые винтовки'),
            KeyboardButton(text = 'Дробовики'),
            KeyboardButton(text = 'Пулеметы')
        ],
        [
            KeyboardButton(text = 'Ключи'),
        ]
        [
             KeyboardButton(text = 'Остановить выгрузку товаров')
        ]
        ]
    keyboard = ReplyKeyboardMarkup(keyboard = buttons, resize_keyboard = True)
    await message.answer(config.START_MESSAGE, reply_markup = keyboard)

@router.message(Command(commands = ['help']))
async def process_help_command(message : Message):
    await message.answer(config.HELP_MESSAGE)

@router.message()
async def process_menu_command(message : Message):
    global msg

    if message.text in config.buttons_text:
        msg = await message.answer(text = 'Please waiting...')
        data = parser.get_weapons_data(parser.get_offset_url(config.buttons_dict[message.text]))
        await msg.delete()

        for index, item in enumerate(data):
            
            await message.answer(text = 
                f'{hlink(item[0], item[1])}\n'
                f'{hbold('🥂Скидка🥂: ')}{item[2][1]} %\n'
                f'{hbold('💲Цена💲: ')}{item[2][0]}',
                parse_mode= ParseMode.HTML
            )
            await sleep(1)

        button = [[InlineKeyboardButton(text = 'Добавить ещё вариантов', callback_data = ButtonAdd(theme = message.text, offset = 60).pack())]]
        keyboard = InlineKeyboardMarkup(inline_keyboard = button)
        msg = await message.answer(text = 'Поиск завершен!', reply_markup = keyboard)

@router.callback_query(ButtonAdd.filter())
async def process_add_command(callback : CallbackQuery, callback_data : ButtonAdd):
    try:
        global msg
        data = parser.get_weapons_data(parser.get_offset_url(config.buttons_dict[callback_data.theme], offset = callback_data.offset))
        await msg.delete()

        for index, item in enumerate(data):
                
                await callback.message.answer(text = 
                    f'{hlink(item[0], item[1])}\n'
                    f'{hbold('🥂Скидка🥂: ')}{item[2][1]} % \n'
                    f'{hbold('💲Цена💲: ')}{item[2][0]}',
                    parse_mode= ParseMode.HTML
                )
                await sleep(1)

        button = [[InlineKeyboardButton(text = 'Добавить ещё вариантов', callback_data = ButtonAdd(theme = callback_data.theme, offset = callback_data.offset + 60).pack())]]
        keyboard = InlineKeyboardMarkup(inline_keyboard = button)
        msg = await callback.message.answer(text = 'Поиск завершен!', reply_markup = keyboard)
    except:
        pass

    
