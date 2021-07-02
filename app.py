import telebot
from extensions import val,TOKEN
from utils import CryptoConverter, APIException


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def test(message: telebot.types.Message):
    text = f'Чтобы конвертировать валюту отправьте боту сообшение в формате:<1> <2> <3> \
            \n<Валюта для продажи> \
            \n<Валюта для покупки> \
            \n<Кол-во валюты для продажи> \
            \n {"-"* 39} \
            \n Пример: Рубль Доллар 100 \
            \n {"-"* 39} \
            \n Список доступных валют по \n команде: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    separator = '-' * 34
    text = f'Доступные валюты:\n{separator}'
    for key, value in val.items():
        currency_value = f'{key} [{value}]'
        text ='\n'.join((text, currency_value, separator ))

    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Больше/меньше 3-ёх параметров.')
        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except APIException as exp:
        bot.reply_to(message, f'Ошибка пользователя.\n{exp}')

    except Exception as exp:
        bot.reply_to(message, f'Не удалось обработать валюту\n {exp}')
    else:
        text = f'Получаем:\n{amount} {val[quote]} = {total_base} {val[base]} \n /values'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)













