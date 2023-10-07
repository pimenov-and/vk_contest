"""
ByteMachine.

12 конкурс в VK-группе ByteMachine.
"""
import vk_contest
import vk_auth


__author__ = "EnergyLabs"
__version__ = "0.9217"
__email__ = "energy.labs@yandex.ru"


def run_contest_12():
    # Заполнение конфигурационных данных
    data = vk_contest.ContestData()
    data.login = vk_auth.get_login()
    data.password = vk_auth.get_password()
    data.group_id = -203791769
    data.post_id = 10690
    data.winner_count = 5

    # Розыгрыш
    vk_contest.run_contest(data)
