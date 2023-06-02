import telebot
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['help', 'start'])
def start_help(message: telebot.types.Message):
    text = 'Вместо хелпы и приветствия:\n\
Это болванка для бота Московского зоопарка\n\
Нам надо дружно сделать из него конфетку)))'
    bot.reply_to(message, text)

bot.polling()