import telebot
from telebot import types

bot = telebot.TeleBot('5344280242:AAEvntH7F66HRMyfSd5X8bKgP0X38RzfWbk')


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    keyboard = types.InlineKeyboardMarkup()
    button_rules = types.InlineKeyboardButton(text="Правила", callback_data="rules")
    button_reg = types.InlineKeyboardButton(text="Регистрация", callback_data="reg")
    keyboard.add(button_rules, button_reg)
    bot.send_message(message.chat.id, "Добро пожаловать на турнир КазНУ!", reply_markup=keyboard)


@bot.inline_handler(lambda query: len(query.query) > 0)
def query_text(query):
    kb = types.InlineKeyboardMarkup()
    # Добавляем колбэк-кнопку с содержимым "test"
    kb.add(types.InlineKeyboardButton(text="Нажми меня", callback_data="test"))
    results = []
    single_msg = types.InlineQueryResultArticle(
        id="1", title="Press me",
        input_message_content=types.InputTextMessageContent(message_text="Я – сообщение из инлайн-режима"),
        reply_markup=kb
    )
    results.append(single_msg)
    bot.answer_inline_query(query.id, results)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data == "test":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
    # Если сообщение из инлайн-режима
    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")


if __name__ == '__main__':
    bot.infinity_polling()
