import telebot
from games import live, upcoming, results, userans
from datetime import datetime, timedelta

bot = telebot.TeleBot('6481972129:AAFrjvY6nd4KM5vAT0RPSLq6uE1zlu9BaoY')


@bot.message_handler(commands=['start'])
def start(message):
    buttons = ['Текущие игры', 'Предстоящие игры', 'Прошедшие игры', 'Турниры']
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for button in buttons:
        keyboard.add(button)

    bot.send_message(message.chat.id, 'Выберите раздел:', reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == 'Текущие игры')
def game_selection_live(message):
    games, id_live = live()
    print(id_live)
    live_game_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for game in games:
        button = telebot.types.KeyboardButton(" vs ".join(game))
        live_game_keyboard.add(button)
    bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=live_game_keyboard)


@bot.message_handler(func=lambda message: message.text == 'Предстоящие игры')
def game_selection_up(message):
    pick_date_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [today, (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'),
               (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d'),
               (datetime.today() + timedelta(days=3)).strftime('%Y-%m-%d')]
    for button in buttons:
        pick_date_keyboard.add(button)
    bot.send_message(message.chat.id, 'Выберите дату игры:', reply_markup=pick_date_keyboard)
    bot.register_next_step_handler(message, today_up)


def today_up(message):
    res_up = upcoming()
    game_keyboard = userans(res_up[message.text])
    bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=game_keyboard)


@bot.message_handler(func=lambda mess: mess.text == (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d'))
def tomorrow_up(mess):
    res_up1 = upcoming()
    print(upcoming())
    game_keyboard1 = userans(res_up1[mess.text])
    bot.send_message(mess.chat.id, 'Выберите игру:', reply_markup=game_keyboard1)


@bot.message_handler(func=lambda message: message.text.split('vs') in upcoming().values())
def aea(message):
    print('123')

    @bot.message_handler(func=lambda mess: message.text == (datetime.today() + timedelta(days=2)).strftime('%Y-%m-%d'))
    def tomorrow1_up(mess):
        game_keyboard2, id_tmrw1 = userans(upcoming()[mess.text])
        bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=game_keyboard2)

    @bot.message_handler(func=lambda mess: message.text == (datetime.today() + timedelta(days=3)).strftime('%Y-%m-%d'))
    def tomorrow2_up(mess):
        game_keyboard3, id_tmrw2 = userans(upcoming()[mess.text])
        bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=game_keyboard3)


@bot.message_handler(func=lambda message: message.text == 'Прошедшие игры')
def game_selection_pr(message):
    pick_date_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    buttons = [today, (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'),
               (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d'),
               (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')]
    for button in buttons:
        pick_date_keyboard.add(button)
    bot.send_message(message.chat.id, 'Выберите дату игры:', reply_markup=pick_date_keyboard)
    bot.register_next_step_handler(message, today_rs)


def today_rs(message):
    games, id_today_rs = results()[message.text]
    game_keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for game in games:
        button = telebot.types.KeyboardButton(" vs ".join(game))
        game_keyboard.add(button)
    game_keyboard = userans(results()[message.text])
    bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=game_keyboard)

    @bot.message_handler(func=lambda mess: message.text == (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d'))
    def yesterday_rs(mess):
        game_keyboard1, id_ystrd = userans(results()[mess.text])
        bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=game_keyboard1)

    @bot.message_handler(func=lambda mess: message.text == (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d'))
    def yesterday1_rs(mess):
        game_keyboard2, id_ystrd1 = userans(results()[mess.text])
        bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=game_keyboard2)

    @bot.message_handler(func=lambda mess: message.text == (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d'))
    def yesterday2_rs(mess):
        game_keyboard3, id_ystrd2 = userans(results()[mess.text])
        bot.send_message(message.chat.id, 'Выберите игру:', reply_markup=game_keyboard3)

    # elif message.text == 'Турниры':
    #     bot.send_message(message.chat.id, 'Здесь вы можете увидеть информацию о турнирах.')


@bot.message_handler(func=lambda message: message.text.split('vs') in upcoming().values())
def aea(message):
    print('123')


print('Start')
today = datetime.today().strftime('%Y-%m-%d')
print(today)

bot.polling()
