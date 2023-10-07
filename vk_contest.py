"""
ByteMachine.

Функции для проведения конкурса VK в группе ByteMachine.
"""
from __future__ import annotations
import vk_api
import random
from operator import itemgetter


__author__ = "EnergyLabs"
__version__ = "0.9217"
__email__ = "energy.labs@yandex.ru"


class ContestData:
    """Данные, необходимые для проведения конкурса."""

    # Логин VK
    login: str = "login"
    # Пароль VK
    password: str = "password"
    # Идентификатор группы VK
    group_id: int = 0
    # Идентификатор поста группы VK
    post_id: int = 0
    # Количество победителей
    winner_count: int = 5


def get_vk_api(data: ContestData):
    """Подключение к VK."""
    my_login = data.login
    my_password = data.password
    vk_session = vk_api.VkApi(login=my_login, password=my_password, app_id=2685278)
    vk_session.auth()
    return vk_session.get_api()


def get_user_info(profile: dict) -> str:
    """Получение информации о пользователе из профиля."""
    first_name = profile["first_name"]
    last_name = profile["last_name"]
    id = profile["id"]
    return f"{first_name} {last_name} <id{id}>"


def get_users(vk, data: ContestData) -> list:
    """Получение пользователей, оставивших комментарии."""
    users = []
    comment_offset = 0
    while True:
        comments = vk.wall.getComments(owner_id=data.group_id, v=5.131, post_id=data.post_id, extended=1, count=100, sort="asc", offset=comment_offset)
        item_count = len(comments["items"])
        if item_count == 0:
            break
        comment_offset += item_count    
        for p in comments["profiles"]:
            user = get_user_info(p)
            if user not in users:
                users.append(user)
    return users


def print_users(users: list) -> None:
    """Печать пользователей."""
    for user in users:
        print(user)
    print(f"*** Участники: {len(users)} ***")


def sort_players(players: list) -> None:
    """Сортировка игроков по баллам."""
    players.sort(key=itemgetter(1), reverse=True)


def print_winners(winners: list, data: ContestData) -> None:
    """Вывод победителей."""
    print("*** Призёры ***")
    count = min(len(winners), data.winner_count)
    for i in range(count):
        winner = winners[i]
        print(f"{i + 1}. {winner[0]}. 1000 рублей и кубок ВК")


def users_to_players(users: list) -> list:
    """Конвертация пользователей в игроков."""
    return [[u,0] for u in users]


def scoring_players(players: list) -> None:
    """Начисление баллов игрокам."""
    random.seed()
    for i in range(50000000):
        index = random.randint(0, len(players) - 1)
        player = players[index]
        player[1] += 1
        if i % 1000000 == 0:
            print(f"- {i // 1000000 + 1} -")


def run_contest(data: ContestData) -> None:
    """Запуск розыгрыша."""

    # Подключение к VK
    vk = get_vk_api(data)

    # Получение пользователей, оставивших комментарии
    users = get_users(vk, data)
    print_users(users)

    # Построение списка с баллами
    players = users_to_players(users)

    # Случайное задание баллов участникам
    scoring_players(players)

    # Сортировка по баллам
    sort_players(players)

    # Вывод участников с местами
    print_winners(players, data)
