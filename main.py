# Устанавливаем библиотеку TelegramBotAPI
# pip install pyTelegramBotAPI
# Устанавливаем библиотеку aiogram 3
# pip install -U --pre aiogram
# Импортируем классы и методы
from aiogram import Bot, Dispatcher
from aiogram.filters import Text, Command
from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup,
                           InlineKeyboardButton,
                           InlineKeyboardMarkup, CallbackQuery)
from aiogram.types import Message
from config import token  # из файла config.py забираем нашу переменную с токеном

import random
# pip freeze > requirements.txt


# Создаем объекты бота и диспетчера
bot: Bot = Bot(token)
dp: Dispatcher = Dispatcher()

# Количество попыток, доступных пользователю в игре
ATTEMPTS: int = 5

money: int = 100
bet:int = money//10

# словарь с данными пользователей
users: dict = {}


# Функция рандомного числа
def get_random_number():
    return random.randint(0, 18)


# Функция рандомного цвета
def get_random_color():
    return random.choice(('черный', 'красный'))


# Создаем объекты кнопок Да, Нет
button_yes: KeyboardButton = KeyboardButton(text='Давай!')
button_no: KeyboardButton = KeyboardButton(text='Не хочу')

# Создаем объект клавиатуры, добавляя в него кнопки Давай!, Не хочу
keyboard_yes_no: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_yes, button_no]],
    resize_keyboard=True,
    one_time_keyboard=True)

# Создаем объекты кнопок Легкий и Сложнее
button_easy: KeyboardButton = KeyboardButton(text='Легкий!')
button_hard: KeyboardButton = KeyboardButton(text='Сложнее')
button_fun: KeyboardButton = KeyboardButton(text='Веселый)')


# Создаем объект клавиатуры, добавляя в него кнопки Легкий и Сложнее и Веселый
keyboard_easy_hard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[button_easy, button_hard,button_fun]],
    resize_keyboard=True,
    one_time_keyboard=True)

# Создаем объекты инлайн-клавиатуры цвета
button_red: InlineKeyboardButton = InlineKeyboardButton(text='КРАСНЫЙ 🟥', callback_data='красный')

button_black: InlineKeyboardButton = InlineKeyboardButton(text='ЧЕРНЫЙ ⬛️', callback_data='черный')

button_green: InlineKeyboardButton = InlineKeyboardButton(text='ЗЕЛЕНЫЙ 🟩', callback_data='зеленый')

button_bet: InlineKeyboardButton = InlineKeyboardButton(text=(f'Сделайте ставку {bet} р.💵'), callback_data='Ставка')

# Создаем объект инлайн клавиатуры красный-черный
keyboard_color: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_red, button_black]],
    resize_keyboard=True)

# Создаем объект инлайн клавиатуры зеленый
keyboard_green: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_green]], resize_keyboard=True)

# Создаем объект инлайн клавиатуры Ставка
keyboard_bet: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[button_bet]], resize_keyboard=True)

# Этот хэндлер будет срабатывать на команду "/start"
# и отправлять в чат клавиатуру
@dp.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer((f'Привет, {message.chat.first_name}! \n'
                          f'Давай сыграем в "Казино"?\n\n'
                          'Чтобы получить правила игры и список доступных '
                          'команд - смотрите МЕНЮ \n'
                          'или отправьте команду /help'))
    await message.answer('Выберите действие', reply_markup=keyboard_yes_no)
    await message.answer(text='👇')

    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                       'secret_color': None,
                                       'attempts': None,
                                       'layer': None,
                                       'money': None,
                                       'user_number': None,
                                       'user_color': None,
                                       'total_games': 0,
                                       'wins': 0}
    print(users)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer((f'Правила игры:\n\n'
                          f'Я загадываю число от 1 до 18\n'
                          f'и цвет КРАСНЫЙ или ЧЕРНЫЙ \n'
                          f'или 0 (ZERO)\n'
                          f'а вам нужно сделать выбор\n\n'
                          f'У вас есть {ATTEMPTS} попыток на легком уровне\n'
                          f'и {ATTEMPTS - 2} попытки на уровне сложнее.\n\n'
                          f'На ВЕСЕЛОМ уровне всего {ATTEMPTS - 3} попытки, но\n'
                          f'есть возможность выйграть ДЕНЬГИ 💵💵💵'
                          f'Доступные команды:\n'
                          f'/start - начать игру \n'
                          f'/help - правила игры и список команд\n'
                          f'/cancel - выйти из игры\n'
                          f'/stat - посмотреть статистику\n\n'
                          f'Давай сыграем? 👇'), reply_markup=keyboard_yes_no)


# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(f'Всего игр сыграно: {users[message.chat.id]["total_games"]}\n'
                          f'Игр выиграно: {users[message.chat.id]["wins"]}\n'
                          f'У Вас денег: {users[message.chat.id]["money"]} р.')


# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры. Если захотите сыграть '
                             'снова - напишите об этом', reply_markup=keyboard_yes_no)
        await message.answer(text='👇')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('А мы итак с вами не играем. '
                             'Может, сыграем разок?', reply_markup=keyboard_yes_no)
        await message.answer(text='😉')


# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(Text(text=['Да', 'Давай!', 'Сыграем', 'Игра', 'Играть'], ignore_case=True))  # игнор регистра True
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer((f'Выберите уровень сложности\n\n'
                              f'на ЛЕГКОМ уровне - {ATTEMPTS} попыток\n'
                              f'на уровне СЛОЖНЕЕ {ATTEMPTS - 2} попытки\n'
                              f'на ВЕСЕЛОМ уровне на старте я дарю вам {money} р. 💵💵💵, \n'
                              f'а у вас {ATTEMPTS - 3} попытки и возможность сделать ставку {bet} р. 💵\n'
                              f'если победите - УДВОИТЕ ставку!!! 🤑'),
                             reply_markup=keyboard_easy_hard)
        await message.answer(text='👇')
    else:
        await message.answer('Пока мы играем в игру я могу '
                             'реагировать только на числа от 1 до 18 '
                             'и команды /cancel и /stat')


# Этот хэндлер будет срабатывать на выбор уровня сложности
@dp.message(Text(text=['Легкий!', 'Сложнее', 'Веселый)'], ignore_case=True))  # игнор регистра True
async def process_easy_hard(message: Message):
    users[message.from_user.id]['layer'] = message.text
    await message.answer(f'Ура!\n\nЯ загадал число от 1 до 18,\n'
                         f'и цвет "ЧЕРНЫЙ ⬛️", "КРАСНЫЙ 🟥" \n\n'
                         f'или \n\n'
                         f'0️⃣ (ZERO) - всегда "ЗЕЛЕНЫЙ 🟩 "😜 \n\n')
    if message.text == 'Легкий!':
        users[message.from_user.id]['attempts'] = ATTEMPTS
        txt = 'попыток'
        await message.answer(f'У вас {users[message.from_user.id]["attempts"]} {txt}\n'
                             f'попробуй угадать!\n\n'
                             f'Жду число!!! 👇')
    if message.text == 'Сложнее':
        users[message.from_user.id]['attempts'] = ATTEMPTS - 2
        txt = 'попытки'
        await message.answer(f'У вас {users[message.from_user.id]["attempts"]} {txt}\n'
                             f'попробуй угадать!\n\n'
                             f'Жду число!!! 👇')
    if message.text == 'Веселый)':
        users[message.from_user.id]['attempts'] = ATTEMPTS - 3
        if users[message.from_user.id]['money'] == None:
            users[message.from_user.id]['money'] = money
        txt = 'попытки'
        await message.answer((f'У Вас {users[message.from_user.id]["money"]} р. 💵💵💵\n'
                             f'Вы делаете ставку в {bet} р. 💵 и если побеждаете - \n'
                             f'УДВАИВАЕТЕ ставку!!! 🤑🤑🤑\n\n'),reply_markup=keyboard_bet)
        print(message)

    users[message.from_user.id]['in_game'] = True
    users[message.from_user.id]['secret_number'] = get_random_number()
    if users[message.from_user.id]['secret_number'] == 0:
        users[message.from_user.id]['secret_color'] = 'зеленый'
    else:
        users[message.from_user.id]['secret_color'] = get_random_color()
    print(users)

@dp.callback_query(Text(text=['Ставка']))
async def process_bet(callback:CallbackQuery):
    print('Выполняется process_bet')
    print(callback)
    if users[callback.message.chat.id]['money'] >= bet:
        users[callback.message.chat.id]['money'] -= bet
        print('Ставка принята')
        await callback.message.answer('Ставка принята')
        await callback.message.answer(f'У вас {users[callback.message.chat.id]["attempts"]} попытки\n'
                                      f'попробуй угадать!\n\n'
                                      f'Жду число!!! 👇')
    else:
        await callback.message.answer((f'Извините, у Вас недостаточно денег(\n'
                              f'Перезапустите бот, нажав /start или\n'
                             f'выберите другой уровень игры'), reply_markup=keyboard_easy_hard)

# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(Text(text=['Нет', 'Не хочу', 'Не', 'Не буду'], ignore_case=True))  # игнор регистра True
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль :(\n\nЕсли захотите поиграть - просто '
                             'напишите об этом', reply_markup=keyboard_yes_no)
        await message.answer(text='👇')
    else:
        await message.answer('Мы же сейчас с вами играем. Присылайте, '
                             'пожалуйста, числа от 1 до 18)')
        await message.answer(text='😉')


# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 18
@dp.message(lambda x: x.text and x.text.isdigit() and 0 <= int(x.text) <= 18)
# фильтр значений по содержимому text, цифры и диапазон
async def process_number_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['user_number'] = message.text
        if message.text == '0':
            await message.answer(text='0 всегда зеленый! 😉 Подтвердите цвет! 👇',
                                 reply_markup=keyboard_green)
        else:
            await message.answer(text='А теперь выберите цвет! 👇',
                                 reply_markup=keyboard_color)
    else:
        await message.answer('Мы еще не играем. Хотите сыграть? 👇', reply_markup=keyboard_yes_no)
        await bot.send_sticker(message.from_user.id,
                               sticker='CAACAgIAAxkBAAMYZChQohHyObLiA3AHNPIJ2JerpM8AAuAAA2GDYwY-cwIBW2KNuS8E')


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'красный' или 'черный' или 'зеленый'
@dp.callback_query(lambda callback: callback.data)
async def process_color_answer(callback: CallbackQuery):
    if users[callback.message.chat.id]['in_game']:
        users[callback.message.chat.id]['user_color'] = callback.data
        print(users[callback.message.chat.id]['attempts'])
        await callback.message.answer(text=f"Вы выбрали "
                                           f"{users[callback.message.chat.id]['user_number']} "
                                           f"{users[callback.message.chat.id]['user_color']}")
        print(users)
        if users[callback.message.chat.id]['user_color'] == users[callback.message.chat.id]['secret_color']:
            if int(users[callback.message.chat.id]['user_number']) == users[callback.message.chat.id]['secret_number']:
                users[callback.message.chat.id]['in_game'] = False
                users[callback.message.chat.id]['total_games'] += 1
                users[callback.message.chat.id]['wins'] += 1
                if users[callback.message.chat.id]['layer'] == 'Веселый)':
                    users[callback.message.chat.id]['money'] += bet*3
                    await callback.message.answer(text=(f'Ура!!! Вы ВЫЙГРАЛИ {bet*2} р.! 😍\n\n'
                                                        f'Может, сыграем еще? 👇'),reply_markup=keyboard_yes_no)
                    await callback.message.answer(text= '🤑')
                else:
                    text = ('Ура!!! Вы ВЫЙГРАЛИ! 😍\n\n'
                            'Может, сыграем еще? 👇')
                    sticker = 'CAACAgIAAxkBAAMSZChPJFJ_gpcIwkkvHkSuvSlw5NUAAgUBAAJhg2MGwbf5qhfi9HEvBA'
                    await callback.message.answer(text=text, reply_markup=keyboard_yes_no)
                    await bot.send_sticker(callback.message.chat.id, sticker=sticker)
                # отправляем статистику
                await process_stat_command(callback.message)
            elif int(users[callback.message.chat.id]['user_number']) > users[callback.message.chat.id]['secret_number']:
                users[callback.message.chat.id]['attempts'] -= 1
                text = (f'Вы угадали цвет!!! 😜 \n'
                        f'Но не угадали число( 😢\n\n'
                        f'Мое число меньше ⬇️\n'
                        f'у вас осталось {users[callback.message.chat.id]["attempts"]} попытки')
                await callback.message.answer(text=text)
            elif int(users[callback.message.chat.id]['user_number']) < users[callback.message.chat.id]['secret_number']:
                users[callback.message.chat.id]['attempts'] -= 1
                text = (f'Вы угадали цвет!!! 😜 \n'
                        f'Но не угадали число( 😢\n\n'
                        f'Мое число больше ⬆️\n'
                        f'у вас осталось {users[callback.message.chat.id]["attempts"]} попытки')
                await callback.message.answer(text=text)
        else:
            if int(users[callback.message.chat.id]['user_number']) == users[callback.message.chat.id]['secret_number']:
                users[callback.message.chat.id]['attempts'] -= 1
                text = (f'Вы угадали число!! 😜 \n'
                        f'Но не угадали цвет( 😢\n\n'
                        f'у вас осталось {users[callback.message.chat.id]["attempts"]} попытки')
                await callback.message.answer(text=text)
            elif int(users[callback.message.chat.id]['user_number']) > users[callback.message.chat.id]['secret_number']:
                users[callback.message.chat.id]['attempts'] -= 1
                text = (f'Вы не угадали цвет и число 😢\n\n'
                        f'Мое число меньше ⬇️\n'
                        f'у вас осталось {users[callback.message.chat.id]["attempts"]} попытки')
                await callback.message.answer(text=text)
            elif int(users[callback.message.chat.id]['user_number']) < users[callback.message.chat.id]['secret_number']:
                users[callback.message.chat.id]['attempts'] -= 1
                text = (f'Вы не угадали цвет и число 😢\n\n'
                        f'Мое число больше ⬆️\n'
                        f'у вас осталось {users[callback.message.chat.id]["attempts"]} попытки')
                await callback.message.answer(text=text)
        if users[callback.message.chat.id]['attempts'] == 0:
            users[callback.message.chat.id]['in_game'] = False
            users[callback.message.chat.id]['total_games'] += 1
            if users[callback.message.chat.id]['layer'] == 'Веселый)':
                await callback.message.answer('Увы, ставка не сыграла 😢')
            text = (f'К сожалению, у вас больше не осталось попыток. 😢\n'
                    f'Вы проиграли( \n\n'
                    f'Мой вариант был {users[callback.message.chat.id]["secret_number"]} '
                    f'{users[callback.message.chat.id]["secret_color"]}\n\n'
                    f'Давайте сыграем еще? 👇')
            sticker = 'CAACAgIAAxkBAAMWZChPyvJ8we6C7SS0ZoIG2gHTytAAAloFAAI_lcwKGxa5hb0gw50vBA'
            await callback.message.answer(text=text, reply_markup=keyboard_yes_no)
            await bot.send_sticker(callback.message.chat.id, sticker=sticker)
            # отправляем статистику
            await process_stat_command(callback.message)


# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_another_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы же сейчас с вами играем. '
                             'Присылайте, пожалуйста, числа от 1 до 18\n'
                             'или пользуйтесь кнопками выбора цвета')
        await message.answer(text='😉')
    else:
        await message.answer('Я довольно ограниченный бот, давайте '
                             'просто сыграем в игру?')
        await message.answer(text='👇')


# Запускаем бота
if __name__ == '__main__':
    dp.run_polling(bot)
