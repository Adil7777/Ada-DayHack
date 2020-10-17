"""import tools"""
from aiogram import Bot, Dispatcher, executor
from messages import *
from InstagramScrapper import InstaLoader
import logging
import random
import smtplib

from db import DataBase

"""Initialization"""

code = ''


def create_code():
    code = ''
    for i in range(0, 16):
        char_or_int = random.choice([True, False])
        if char_or_int:
            code += str(random.randint(0, 9))
        else:
            code += chr(ord('a') + random.randint(0, 25))
    return code


def send_mail(send_to_email, text):
    EMAIL = 'ada.teensinai.helpingeye@gmail.com'
    PASSWORD = 'hJgX&*W2Yj'

    try:
        message = str(text)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(EMAIL, PASSWORD)

        server.sendmail(EMAIL, send_to_email, message)
        server.quit()
        return True
    except Exception as e:
        return e


TOKEN = '1288952697:AAHxWvT1-X-rR3pGp7p5DYvQ4Lka7Bv6Kno'

logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN)
dp = Dispatcher(bot)
Database = DataBase()
Database.init_db()


@dp.message_handler(commands=['start'])
async def start(message):
    await bot.send_message(message.chat.id, WELCOME_MESSAGE)


@dp.message_handler(commands=['register'])
async def register(message):
    name, surname, account, email = message.text.replace('/register ', '').split(' ')
    print(name, surname, account, email)
    Database.add_user(message.chat.id, name, surname, account, email)
    await bot.send_message(message.chat.id, REGISTER)


@dp.message_handler(commands=['send_private_policy'])
async def send_private_policy(message):
    f = open('Agreement on the processing of personal data.txt', 'rb')
    await bot.send_document(message.chat.id, f)


@dp.message_handler(commands=['check_account'])
async def check_account(message):
    try:
        account = Database.get_user(message.chat.id)[4]
        await bot.send_message(message.chat.id, 'Getting information from tha page\n\nIt would take some time')
        result = get_prediction(account)
        await bot.send_message(message.chat.id, result)
    except Exception as e:
        await bot.send_message(message.chat.id, 'You are not registered')


@dp.message_handler(commands=['send_code'])
async def send_code(message):
    global code
    email = message.text.replace('/send_code ', '')
    code = create_code()
    send_mail(email, code)
    await bot.send_message(message.chat.id, SEND_CODE)


@dp.message_handler(commands=['check_code'])
async def check_code(message):
    user_code = message.text.replace('/check_code ', '')
    if user_code == code:
        await bot.send_message(message.chat.id, 'You have registered')
    else:
        await bot.send_message(message.chat.id, WRONG_CODE)


def get_prediction(account):
    loader = InstaLoader(account)
    loader.get_pictures()
    posts = loader.all_words()
    # for i in posts.split(' '):
    #     print(i.lower())
    # print('ok')
    images, texts = loader.get_files()
    enough = (len(texts) + len(images)) // 4 * 3
    sign_words_counter = 0
    for i in posts.split(' '):
        if i.lower() in SIGN_WORDS:
            sign_words_counter += 1
    print(sign_words_counter)

    rgbs = loader.check_image()

    for i in rgbs:
        r, g, b = i
        if r <= 128 and g <= 128 and b <= 128:
            sign_words_counter += 1
    print(sign_words_counter)

    if sign_words_counter >= enough:
        return random.choice(SEND_BAD_RESULT)
    else:
        return random.choice(SEND_GOOD_RESULT)


if __name__ == "__main__":
    print('program starting')
    executor.start_polling(dp, skip_updates=True)
