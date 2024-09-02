import telebot
from config import keys, TOKEN
from extensions import APIException, get_price

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(massage: telebot.types.Message):
    text = 'Чтобы начать работу введите комманду боту в слудующем формате: \n \n \
<имя валюты, цену которой Вы хотите узнать> \
<имя валюты, в которой надо узнать цену первой> <количество первой валюты> \n\nУвидеть список всех доступных валют: /values'
    bot.reply_to(massage, text)

@bot.message_handler(commands=['values'])
def values(massage: telebot.types.Message):
    text = 'Доступные валюты:' '\n'
    for key in keys.keys():
        text ='\n'.join((text,key, ))
    bot.reply_to(massage, text)

@bot.message_handler(content_types=['text', ])
def convert(massage: telebot.types.Message):
    try:
        values = massage.text.split(' ')

        if len(values) != 3:
            raise APIException('Недопустимое количество параметров.')

        quote, base, amount = values
        total_base = get_price.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(massage, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(massage, f'Не удалось обработать команду\т{e}')

    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(massage.chat.id, text)

bot.polling()
