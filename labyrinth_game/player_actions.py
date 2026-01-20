"""
Действия игрока в игре Лабиринт

"""

from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room, random_event


def show_inventory(game_state):
    """
    Args:
        game_state (dict): Словарь состояния игры,
        должен содержать ключ 'player_inventory'
    """

    inventory = game_state.get("player_inventory", [])

    if inventory:
        print("Инвентарь игрока:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("Инвентарь пуст.")


def move_player(game_state, direction):
    """
    Args:
        game_state (dict): Состояние игры
        direction (str): Направление движения ('north', 'south', 'west', 'east')
    Returns:
        bool: True если перемещение успешно, False если нет
    """

    current_room_name = game_state["current_room"]
    current_room = ROOMS.get(current_room_name)

    if not current_room:
        print(f'Ошибка: комната "{current_room_name}" не найдена!')
        return False

    exits = current_room.get("exits", {})

    if direction in exits:
        new_room = exits[direction]

        if (
            new_room == "treasure_room"
            and "rusty_key" not in game_state["player_inventory"]
        ):
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return False
        elif (
            new_room == "treasure_room"
            and "rusty_key" in game_state["player_inventory"]
        ):
            print(
                "Вы используете найденный ключ,  чтобы открыть путь в комнату сокровищ."
            )

        if new_room == "secret_room":
            if "library_access" not in game_state.get("solved_puzzles", []):
                print(
                    "Проход в секретную комнату закрыт. "
                    "Нужно решить загадку в библиотеке."
                )
                return False

        game_state["current_room"] = new_room
        game_state["steps"] += 1

        direction_names = {
            "north": "север",
            "south": "юг",
            "west": "запад",
            "east": "восток",
        }
        ru_direction = direction_names.get(direction, direction)
        print(f"Вы пошли на {ru_direction}...")
        print()

        describe_current_room(game_state)

        random_event(game_state)

        return True
    else:
        print(f"Нельзя пойти в этом направлении ({direction}).")
        return False


def use_item(game_state, item_name):
    """
    Args:
        game_state (dict): Состояние игры
        item_name (str): Название предмета для использования
    """
    if item_name == "throne":
        if game_state["current_room"] == "hall":
            print("Вы садитесь на трон. Чувствуете себя королем!")
            print("Это придает вам уверенности.")
            return
        else:
            print("Здесь нет трона.")
            return

    if item_name not in game_state["player_inventory"]:
        print("У вас нет такого предмета.")
        return

    if item_name == "torch":
        print("Стало светлее.")

    elif item_name == "gem":
        print("Самоцвет красиво переливается на свету.")

    elif item_name == "sword":
        print("Вы чувствуете уверенность, держа меч в руках.")

    elif item_name == "ancient_scroll":
        print("Вы читаете древний свиток: 'Код: 4857'")
        if "treasure_code" not in game_state:
            game_state["treasure_code"] = "4857"

    elif item_name == "flower_key":
        if game_state["current_room"] == "hall":
            print("Вы вставляете цветочный ключ в золотую дверь...")
            print("Замок щелкает, и дверь плавно открывается.")
            print("Вы видите перед собой солнечный свет и выход из лабиринта!")
            print("\nВы получили хорошую концовку! ")
            print("Победа! Вы успешно выбрались из лабиринта!")
            print("\nСпасибо за игру!")
            game_state["game_over"] = True
        else:
            print("Здесь нет подходящей двери для этого ключа.")

    elif item_name == "throne":
        if game_state["current_room"] == "hall":
            print("Вы садитесь на трон. Чувствуете себя королем!")
            print("Это придает вам уверенности.")
        else:
            print("Здесь нет трона.")

    elif item_name == "bronze_box":
        print("Вы открыли бронзовую шкатулку.")

        if "rusty_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("rusty_key")
            print("Вы нашли ржавый ключ!")

    else:
        print("Вы не знаете, как использовать этот предмет.")


def take_item(game_state, item_name):
    """
    Args:
        game_state (dict): Состояние игры
        item_name (str): Название предмета для взятия
    """
    current_room_name = game_state["current_room"]

    if current_room_name not in ROOMS:
        print("Ошибка: текущая комната не найдена!")
        return

    current_room = ROOMS[current_room_name]
    items_in_room = current_room.get("items", [])

    if item_name in ["treasure_chest", "throne"]:
        print("Вы не можете поднять это. Это слишком тяжело.")
        return

    if item_name in items_in_room:
        game_state["player_inventory"].append(item_name)

        items_in_room.remove(item_name)

        print(f"Вы подняли {item_name}.")
    else:
        print("Такого предмета здесь нет.")


def get_input(prompt="> "):
    """
    Args:
        prompt (str): Текст приглашения для ввода.
    Returns:
        str: Введенная пользователем строка или "quit" при прерывании.
    """

    try:
        return input(prompt).strip().lower()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
