import logging, telebot
from config import TG_TOKEN
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

bot = telebot.TeleBot(TG_TOKEN);

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


@bot.message_handler(content_types=['text'])
def start(m):
    first_name = m.from_user.first_name

    logger.info("Пользователь %s начал разговор", first_name)

    if first_name:
        bot.send_message(m.from_user.id, f"Hi {first_name}! Welcome!");
    else:
        bot.send_message(m.from_user.id, "Hi Guest! Welcome!");

    keyboard = [
        [
            InlineKeyboardButton("English", callback_data='Eng'),
            InlineKeyboardButton("Українська", callback_data='Ukr'),
            InlineKeyboardButton("Русский", callback_data='Rus'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    bot.send_message(m.from_user.id, "Choose the language of communication", reply_markup = reply_markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == "Eng":
        bot.send_message(call.message.chat.id, "Sorry friend! This bot is made for learning the Python programming language. If you want, help the Ukrainian army")

    elif call.data == "Ukr":
        city = bot.send_message(call.message.chat.id, 'Цей бот прогнозує погоду. Введи, будь ласка, населений пункт для того, щоб дізнатися погоду в ньому')
        bot.register_next_step_handler(city, ukrainian)

    else:
        city = bot.send_message(call.message.chat.id, "Этот бот, предсказывает погоду. Введи, пожалуйста населенный пункт для того, чтобы узнать погоду в нем")
        bot.register_next_step_handler(city, russian)


def ukrainian(city):
    bot.send_message(city.chat.id, f"Чесно кажучи, я не знаю про {city.text}, але я знаю, що над Украъною буде сяяти сонечко перемоги!")


def russian(city):
    bot.send_message(city.chat.id, f"Честно говоря, я не знаю что там {city.text}, но я знаю, что в скором временим, над всеми военно-стратегическими объектами эрефии, будет град!\n\nТ. ч. москалыку, если ты держишь (или держал) оружие против Украины, закупи для себя мусорный пакетик и носи его с собой чтобы то, что от тебя останется, могли собрать в этот пакетик.\n\nНу а если ты мирный житель, то лучше прячься поглубже, хотя...")


if __name__ == '__main__':
    bot.polling(none_stop=True)
