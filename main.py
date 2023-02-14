import sqlite3
import telebot
from telebot import types

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

# cur.execute("""CREATE TABLE IF NOT EXISTS users(
#    chatid INT,
#    nickname TEXT,
#    steam_url TEXT,
#    level INT,
#    accepted INT);
# """)
# conn.commit()

bot = telebot.TeleBot("ApiKey")

clear = '"\'-*\\= '

nickname = False
steam = False
level = False


def admin_markup():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 3
    markup.add(
        types.InlineKeyboardButton("Зареганы вообщем", callback_data="all_count"),
        types.InlineKeyboardButton("Сколько подтвердило", callback_data="accepted_count"),
        types.InlineKeyboardButton("Список подтвердивших", callback_data="accepted_list")
    )
    return markup


def first_page():
    markup = types.InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        types.InlineKeyboardButton("Информация", callback_data="info"),
        types.InlineKeyboardButton("Регистрация", callback_data="registration"),
    )
    return markup


def nick_tosql(chat_id, text):

    for char in clear:
        text = text.replace(char, "")

    global nickname, steam
    nickname = False
    steam = True

    mw = (chat_id, text, None, None, 0)
    cur.execute("insert into users values(?, ?, ?, ?, ?);", mw)
    conn.commit()


def steam_tosql(chat_id, text):

    for char in clear:
        text = text.replace(char, "")

    global steam, level
    steam = False
    level = True

    cur.execute(
        f"""update users 
                    set steam_url = '{text}' 
                    where chatid = {chat_id}"""
    )
    conn.commit()


def level_tosql(chat_id, text):

    for char in clear:
        text = text.replace(char, "")

    global level
    level = False

    cur.execute(
        f"""update users 
                    set level = {text} 
                    where chatid = {chat_id}"""
    )
    conn.commit()


def accept(chat_id):

    cur.execute(
        f"""update users 
                    set accepted = 1
                    where chatid = {chat_id}"""
    )
    conn.commit()


def get_accepted_count():
    cur.execute('select * from users')
    all_user_list = cur.fetchall()
    count = 0
    for i in range(len(all_user_list)):
        if all_user_list[i][4] > 0:
            count += 1
    return count


def list_all(chat_id):
    cur.execute("select * from users")
    all_players = cur.fetchall()

    for i in range(len(all_players)):
        bot.send_message(chat_id, f"""Ник: {all_players[i][1]}\nУровень: {all_players[i][3]}""")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "info":
        bot.send_message(
            call.message.chat.id, "Info, bla bla bla", reply_markup=first_page()
        )
    elif call.data == "registration":
        global nickname
        nickname = True
        bot.send_message(call.message.chat.id, "Напишите ваш Никнейм")
    elif call.data == "all_count":
        cur.execute('select * from users')
        bot.send_message(call.message.chat.id, f"Количество зарегистрированных участников - {len(cur.fetchall())}")
    elif call.data == "accepted_count":
        bot.send_message(call.message.chat.id, f"Количество подтвердивших участников - {get_accepted_count()}")
    elif call.data == "accepted_list":
        bot.send_message(call.message.chat.id, "Список участников:")
        list_all(call.message.chat.id)


@bot.message_handler(commands=["start"])
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        "Добро пожаловать на турнир КазНУ!!!",
        reply_markup=first_page(),
    )


@bot.message_handler(commands=["admin"])
def cmd_start(message):
    bot.send_message(
        message.chat.id,
        "Оу, админ?",
        reply_markup=admin_markup(),
    )


@bot.message_handler(func=lambda message: True)
def message_handler_query(message):
    if nickname:
        nick_tosql(message.chat.id, message.text)
        bot.send_message(
            message.chat.id, "Дальше, отправьте ссылку на ваш steam аккаунт"
        )
    elif steam:
        steam_tosql(message.chat.id, message.text)
        bot.send_message(
            message.chat.id,
            "И, последнее, напишите ваш уровень FaceIT (если нет, напишите просто 0)",
        )
    elif level:
        level_tosql(message.chat.id, message.text)
        bot.send_message(
            message.chat.id,
            """Спасибо за регистрацию!
Приходите в такое-то число, и ждите дальнейших инструкции :3""",
        )
    elif message.text.replace(" ", "").lower() == "подтвердить":
        accept(message.chat.id)


if __name__ == "__main__":
    bot.infinity_polling()
