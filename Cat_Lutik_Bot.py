import config
import sqlite3
import locale
import os
from datetime import datetime
from random import randint
from telebot import TeleBot, types


TOKEN = os.getenv('BOT_TOKEN')
bot = TeleBot(token=TOKEN)
locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

# bot = TeleBot(config.token)


# Вносим данные в заранее созданную базу данных
def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute('INSERT OR IGNORE INTO test_table (user_id, user_name, user_surname, username) VALUES (?, ?, ?, ?)',
                   (user_id, user_name, user_surname, username))
    conn.commit()


# Начинаем диалог с ботом, присваиваем переменным данные пользователя и указываем их в качестве аргументов функции db_table_val()
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(
        message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name} ✌️')
    main_buttons(message)

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    db_table_val(user_id=us_id, user_name=us_name,
                 user_surname=us_sname, username=username)


# Создаем кнопки, которые встречают нас при запуске бота
def main_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    what_is_you_Lutik = types.KeyboardButton('Лютик этого дня')
    lutiks_quote = types.KeyboardButton('Цитата этого дня от Лютика')
    vitalik = types.KeyboardButton('Я Виталик и я хочу пор жать')
    markup.add(what_is_you_Lutik, lutiks_quote, vitalik)
    bot.send_message(
        message.chat.id, 'Выбери что ты хочешь получить от Лютика', reply_markup=markup)


# Создаем кнопки, которые встречают нас, когда мы указали что мы Виталик
def vitalik_buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    want_meme = types.KeyboardButton('Хочу мем')
    want_joke = types.KeyboardButton('Хочу анекдот')
    not_vitalik = types.KeyboardButton(
        'Я не Виталик, я заблудился! Не еби меня :с')
    markup.add(want_meme, want_joke, not_vitalik)
    bot.send_message(
        message.chat.id, 'Ну шо, Виталя? Ебать тя будем или выберешь что-нибудь другое?', reply_markup=markup)


# Отдаем пользователю рандомный анекдот из списка анекдотов
def get_joke(list_of_jokes):
    joke_number = randint(0, 10)
    all_jokes, joke = [], []
    for line in list_of_jokes:
        if line != '\n':
            joke.append(line.strip())
        else:
            all_jokes.append(joke)
            joke = []
    all_jokes.append(joke)
    return '\n'.join(all_jokes[joke_number])


# Функция реагирует на отправленные пользователем фото и видео
@bot.message_handler(content_types=['photo', 'video'])
def get_user_photo(message):
    bot.send_message(message.chat.id, 'Вау! Надеюсь, там был твой член 🍆')
    main_buttons(message)


# Функция реагирует на отправленные пользователем голосовые сообщения
@bot.message_handler(content_types=['voice'])
def get_out(message):
    # нужно будет записать голос Лютика и отправлять его, если пользователь отправит нам voice
    audio_for_user = open('D:/Python/Bot_Cat_Lutik/ba-dum-tss.mp3', 'rb')
    bot.send_audio(message.chat.id, audio_for_user)
    main_buttons(message)


# Функция по обработке текста кнопок, которые нажал пользователь
@bot.message_handler(content_types=['text'])
def get_user_text(message):

    if message.text.lower() == 'лютик этого дня':
        photo_description = {1: 'Зубастый', 2: 'Лютик, который сьпит :з', 3: 'Лютик-чушка',
                             4: 'Лютик "Чахлы"', 5: 'Кустарный сцыкун', 6: 'Лютик "Полупокер"',
                             7: 'На раслабоне (полном)'}
        photo_number = datetime.now().isoweekday()
        photo = open(
            f'D:/Python/Telegram_Bot_Cat_Lutik/cat_photo/{str(photo_number)}.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)
        bot.send_message(
            message.chat.id, f'{datetime.now().strftime("%a %d.%m.%Y")} - "{photo_description[photo_number]}"')

    elif message.text.lower() == 'цитата этого дня от лютика':
        quotes = {1: 'Цель всякой жизни есть смерть',
                  2: 'Смерть — это только преувеличенное, резкое, кричащее, грубое выражение того, что мир собою представляет всецело.',
                  3: 'Каждому из нас доступно следующее утешение: смерть так же естественна, как и жизнь, а там, что будет, — это мы увидим.',
                  4: 'Есть два пути избавить вас от страдания: быстрая смерть и продолжительная любовь.',
                  5: 'Существует право, по которому мы можем отнять у человека жизнь, но нет права, по которому мы могли бы отнять у него смерть; это есть только жестокость.',
                  6: 'Тот, кто становится пресмыкающимся червем, может ли затем жаловаться, что его раздавили?',
                  7: 'Смерти меньше всего боятся те люди, чья жизнь имеет наибольшую ценность.'}
        number_of_quote = datetime.now().isoweekday()
        bot.send_message(message.chat.id, quotes[number_of_quote])

    elif message.text.lower() == 'я виталик и я хочу пор жать':
        vitalik_buttons(message)

    elif message.text.lower() == 'хочу мем':
        random_picture = randint(1, 18)
        photo = open(
            f'D:/Python/Telegram_Bot_Cat_Lutik/memes/mem{str(random_picture)}.jpg', 'rb')
        bot.send_photo(message.chat.id, photo)

    elif message.text.lower() == 'хочу анекдот':
        with open('D:/Python/Telegram_Bot_Cat_Lutik/jokes.txt', 'r', encoding='utf-8') as file:
            bot.send_message(message.chat.id, get_joke(file.readlines()))

    elif message.text.lower() == 'я не виталик, я заблудился! не еби меня :с':
        main_buttons(message)

    else:
        bot.send_message(
            message.chat.id, 'Дурачок, нажми на любую кнопку снизу. Твои букавы я читать НЕ-БУ-ДУ!')
        main_buttons(message)


bot.infinity_polling()
