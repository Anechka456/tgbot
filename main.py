import logging
import os

import aiohttp
from dotenv import load_dotenv
from telegram.ext import Application, MessageHandler, filters

load_dotenv()
BOT_TOKEN = os.getenv('token', 'nosecret')

# Запускаем логгирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)

# Добавим необходимый объект из модуля telegram.ext
from telegram.ext import CommandHandler


async def geocoder(update, context):
    geocoder_uri = "http://geocode-maps.yandex.ru/1.x/"
    try:
        response = await get_response(geocoder_uri, params={
            "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
            "format": "json",
            "geocode": update.message.text
        })
        if response['response']['GeoObjectCollection']['metaDataProperty']['GeocoderResponseMetaData']['found'] == '0':
            await update.message.reply_text(
                f'По этому запросу ничего не найдено')
            return
    except Exception as e:
        await update.message.reply_text(
            f'Во время получения данных произошла ошибка {e}. Попробуй повторить запрос позже')
        return

    toponym = response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    coordinates = toponym['Point']["pos"]

    try:
        response_map = f"http://static-maps.yandex.ru/1.x/?spn=0.01,0.01&size=650,450&pt={','.join(coordinates.split())},pm2lbm&l=map"
    except Exception as e:
        await update.message.reply_text(
            f'Во время получения данных произошла ошибка {e}. Попробуй повторить запрос позже')
        return
    await context.bot.send_photo(update.message.chat_id, response_map,
                                 caption="Вот что я нашёл. Что ещё вы хотите увидеть?")


async def get_response(url, params):
    logger.info(f"getting {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return await resp.json()


async def start(update, context):
    await update.message.reply_text(
        "Привет! Я бот-геокодер.\n"
        "Напешите город или какой-либо объект и я пришлю его расположение на карте!",
    )


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT, geocoder))

    # Запускаем приложение.
    application.run_polling()


# Запускаем функцию main() в случае запуска скрипта.
if __name__ == '__main__':
    main()
