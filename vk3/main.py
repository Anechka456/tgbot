import datetime
import os

import requests
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

BOT_TOKEN = 'vk1.a.fiJ9tNTQbXgCsZWBA8j8tg4HWULupOb1k5we06kAWbJIHy3EzhG6dHnCz3DtN2n1vUewIMGEnaJNRrVW3bf-9EIkUQUEe__hIdasO-hAFCwfiFuxGXWVIVUYut8UXrOShaZ0jueEw0ojM8ZcWIgMxCCUL6TouCwFLStRR8ndXDToA6zt8JO0eCdIs-T12f1h1Mm9mBF8fpG59I9K036Pkg'


def get_wikipedia_text(title, lang='ru'):
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{title}"
    headers = {'Accept': 'application/json; charset=utf-8'}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data.get('extract', 'Текст статьи не найден')
        else:
            return f"Ошибка: {response.status_code} - {response.reason}"
    except Exception as e:
        return f"Ошибка запроса: {str(e)}"


def main():
    vk_session = vk_api.VkApi(
        token=BOT_TOKEN)

    longpoll = VkBotLongPoll(vk_session, '230275551')

    for event in longpoll.listen():

        if event.type == VkBotEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            print('Для меня от:', event.obj.message['from_id'])
            print('Текст:', event.obj.message['text'])
            vk = vk_session.get_api()
            response = vk.users.get(user_id=event.obj.message['from_id'], fields='city')[0]
            print(response)
            print(event.obj.message)
            txt = event.obj.message['text'].lower()
            if 'найди' in txt:
                response_viki = get_wikipedia_text(txt.split('найди')[-1].strip())
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=response_viki,
                                 random_id=random.randint(0, 64 * 2))
            else:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Привет, {response['first_name']}!",
                                 random_id=random.randint(0, 64 * 2))
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Напиши команду найди 'запрос' и я найду это информацию в вики",
                                 random_id=random.randint(0, 64 * 2))

if __name__ == '__main__':
    main()