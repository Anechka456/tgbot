import os

import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random

BOT_TOKEN = 'vk1.a.fiJ9tNTQbXgCsZWBA8j8tg4HWULupOb1k5we06kAWbJIHy3EzhG6dHnCz3DtN2n1vUewIMGEnaJNRrVW3bf-9EIkUQUEe__hIdasO-hAFCwfiFuxGXWVIVUYut8UXrOShaZ0jueEw0ojM8ZcWIgMxCCUL6TouCwFLStRR8ndXDToA6zt8JO0eCdIs-T12f1h1Mm9mBF8fpG59I9K036Pkg'
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
            vk.messages.send(user_id=event.obj.message['from_id'],
                             message=f"Привет, {response['first_name']}!",
                             random_id=random.randint(0, 64 * 2))
            if 'city' in response:
                vk.messages.send(user_id=event.obj.message['from_id'],
                                 message=f"Как поживает {event.obj.message['city']}?",
                                 random_id=random.randint(0, 64 * 2))


if __name__ == '__main__':
    main()