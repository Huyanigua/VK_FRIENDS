import requests
import json


class Person:
    def __init__(self, id, first_name, last_name):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name
        }


def get_user_info(user_id: str, token: str, version: str) -> dict:
    params = {
        'access_token': token,
        'v': version,
        'user_ids': user_id,
        'fields': 'first_name,last_name'
    }
    response = requests.get('https://api.vk.com/method/users.get', params=params)
    try:
        return response.json()['response'][0]
    except KeyError:
        return {}


def get_friends(user_id: str, token: str, version: str) -> list:
    params = {
        'access_token': token,
        'v': version,
        'user_id': user_id,
        'fields': 'first_name,last_name'
    }
    response = requests.get('https://api.vk.com/method/friends.get', params=params)
    try:
        return response.json()['response']['items']
    except KeyError:
        return []


def collect_friends_and_their_friends(user_id: str, token: str, version: str) -> dict:
    user_info = get_user_info(user_id, token, version)

    friends_data = {
        'user': {
            'id': user_id,
            'first_name': user_info.get('first_name', ''),
            'last_name': user_info.get('last_name', ''),
            'friends': []
        }
    }

    # Получаем друзей
    friends = get_friends(user_id, token, version)

    for friend in friends:
        friend_id = friend['id']
        first_name = friend.get('first_name', '')
        last_name = friend.get('last_name', '')

        # Создаем объект для друга
        friend_info = {
            'id': friend_id,
            'first_name': first_name,
            'last_name': last_name,
            'friends_of_friend': []
        }

        # Получаем друзей друга
        friends_of_friend = get_friends(friend_id, token, version)

        for fof in friends_of_friend:
            fof_id = fof['id']
            fof_first_name = fof.get('first_name', '')
            fof_last_name = fof.get('last_name', '')

            # Добавляем друга друга в список
            friend_info['friends_of_friend'].append({
                'id': fof_id,
                'first_name': fof_first_name,
                'last_name': fof_last_name
            })

        # Добавляем информацию о друге в общий список
        friends_data['user']['friends'].append(friend_info)

    return friends_data


def save_to_json(data: dict, filename: str):
    with open(filename, 'w', encoding='UTF-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Основная часть программы
TOKEN = ''  # API Токен
VERSION = '5.199'  # Версия API
user_id = '613775434'  # Мой ID

friends_data = collect_friends_and_their_friends(user_id, TOKEN, VERSION)
save_to_json(friends_data, 'friends_data.json')

print(f'Данные о пользователе и его друзьях сохранены в файл friends_data.json')