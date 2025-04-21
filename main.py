# Импортируем необходимые классы.
import datetime
import json
import logging
import os
from random import shuffle

from telegram.ext import Application, MessageHandler, filters
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from random import randrange

load_dotenv()
BOT_TOKEN = os.getenv('token', 'nosecret')

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import CommandHandler, ConversationHandler


filename = input('Введите имя файла с вопросами ')
with open(filename, 'r', encoding='utf-8') as file:
    data = json.load(file)['test']
print('Данные из файла получены')


async def start(update, context):
    context.user_data['result'] = 0  # количество правильных ответов
    context.user_data['questions'] = data.copy()
    shuffle(context.user_data['questions'])
    print(context.user_data['questions'])
    await update.message.reply_text(
        f'Предлагаю пройти тест\n'
        f'Для досрочного завершения отправьте /stop\n'
        f'{context.user_data["questions"][0]["question"]}')
    return 1



async def stop(update, context):
    response_text = 'Ладно. Может быть, начнём сначала?'
    response_keyboard = [['/start']]
    markup = ReplyKeyboardMarkup(response_keyboard)
    await update.message.reply_text(response_text, reply_markup=markup)
    return ConversationHandler.END



async def main_handler(update, context):
    text = update.message.text
    current_question = context.user_data['questions'].pop(0)
    if text == current_question['response']:
        context.user_data['result'] += 1
    if len(context.user_data['questions']) == 0:
        response_text = (f'Вопросы закончились. Ваш результат {context.user_data['result']}/{len(data)}\n'
                         f'Пройдём тест снова?')
        response_keyboard = [['/start']]
        markup = ReplyKeyboardMarkup(response_keyboard)
        await update.message.reply_text(response_text, reply_markup=markup)
        return ConversationHandler.END
    else:
        question = context.user_data['questions'][0]['question']
        await update.message.reply_text(question)
        return 1


def main():
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, main_handler)]
        },
        fallbacks=[CommandHandler('stop', stop)]
    )
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(conversation_handler)

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
