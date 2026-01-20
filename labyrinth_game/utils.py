"""
Вспомогательные функции для игры Лабиринт
"""

import math

from labyrinth_game.constants import ROOMS


def describe_current_room(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """
    current_room_name = game_state.get("current_room", "entrance")

    if current_room_name not in ROOMS:
        print(f"Ошибка: комната '{current_room_name}' не найдена.")
        return

    room = ROOMS[current_room_name]

    print(f"== {current_room_name.upper()} ==")
    print()

    print(room["description"])
    print()

    if room["items"]:
        print("Заметные предметы:")
        for item in room["items"]:
            print(f"  - {item}")
        print()

    if room["exits"]:
        print("Выходы:")
        for direction, target_room in room["exits"].items():
            print(f"  {direction} -> {target_room}")
        print()

    puzzle = room.get("puzzle")
    if puzzle:
        print("Кажется, здесь есть загадка (используйте команду solve).")
        print()


def solve_puzzle(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """

    current_room_name = game_state["current_room"]

    if current_room_name not in ROOMS:
        print("Ошибка: текущая комната не найдена!")
        return

    current_room = ROOMS[current_room_name]

    if "puzzle" not in current_room:
        print("Загадок здесь нет.")
        return

    puzzle_data = current_room["puzzle"]

    if len(puzzle_data) == 2:
        puzzle_question, correct_answer = puzzle_data
        reward_item = "reward"
    elif len(puzzle_data) == 3:
        puzzle_question, correct_answer, reward_item = puzzle_data
    else:
        print("Некорректные данные загадки.")
        return

    print(puzzle_question)

    user_answer = input("Ваш ответ: ").strip().lower()

    if correct_answer == "10" and user_answer == "десять":
        is_correct = True
    else:
        is_correct = user_answer == correct_answer.lower()

    if is_correct:
        print("Верно! Загадка решена.")

        del current_room["puzzle"]

        if current_room_name == "entrance":
            current_room["exits"]["east"] = "hallway"
            print("Дверь открывается! Вы можете войти в лабиринт.")
            print("Вход:")
            print("    east -> hallway")

        elif current_room_name == "library":
            if "solved_puzzles" not in game_state:
                game_state["solved_puzzles"] = []
            game_state["solved_puzzles"].append("library_access")
            print("Книжная полка сдвигается, открывая проход в секретную комнату!")

        elif current_room_name == "trap_room":
            game_state["player_inventory"].append("gem")
            print("Вы получили: gem")

        elif current_room_name == "hall":
            print("Вы произносите ответ на загадку...")
            print("Золотая дверь с грохотом открывается!")
            print("Вы делаете шаг в темноту и...")
            print("\nВы получили плохую концовку!")
            print(
                "Вы открываете дверь,"
                " делаете шаг в темноту и не чувствуете почву под ногами!"
            )
            print("Вы упали в бездонную пропасть!")
            print("\nК сожалению, ваше путешествие завершилось трагически...")
            game_state["game_over"] = True
            return
    else:
        print("Неверно. Попробуйте снова.")

    if current_room_name == "trap_room":
        trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """

    current_room_name = game_state["current_room"]

    if current_room_name not in ROOMS:
        print("Ошибка: текущая комната не найдена!")
        return

    current_room = ROOMS[current_room_name]

    if "treasure_chest" not in current_room.get("items", []):
        print("Здесь нет сундука с сокровищами.")
        return

    if "treasure_key" in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")

        current_room["items"].remove("treasure_chest")

        if "flower_key" not in game_state["player_inventory"]:
            game_state["player_inventory"].append("flower_key")
            print("Вы нашли золотой ключ в виде цветка!")

        print("В сундуке сокровище!")
        return

    print("Сундук заперт. У вас нет ключа.")
    response = input("Ввести код? (да/нет): ").strip().lower()

    if response == "да":
        if "puzzle" not in current_room:
            print("Сундук невозможно открыть без ключа или кода.")
            return

        _, correct_code = current_room["puzzle"]
        user_code = input("Введите код: ").strip()

        if user_code == correct_code:
            print("Код принят! Сундук открыт.")

            current_room["items"].remove("treasure_chest")

            if "flower_key" not in game_state["player_inventory"]:
                game_state["player_inventory"].append("flower_key")
                print("Вы нашли золотой ключ в виде цветка!")

            print("Вы нашли сокровище!")
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")


def trigger_trap(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """
    print("Ловушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]

    PROTECTED_ITEMS = ["rusty_key", "bronze_box"]
    TRAP_MODULO = 10
    TRAP_DAMAGE_THRESHOLD = 2

    if inventory:
        losable_items = [item for item in inventory if item not in PROTECTED_ITEMS]

        if losable_items:
            seed = game_state.get("steps", 0)
            modulo = len(losable_items)

            random_index = pseudo_random(seed, modulo)

            lost_item = losable_items[random_index]
            inventory.remove(lost_item)
            print(f"Вы потеряли предмет: {lost_item}!")
        else:
            seed = game_state.get("steps", 0)

            random_value = pseudo_random(seed, TRAP_MODULO)

            if random_value < TRAP_DAMAGE_THRESHOLD:
                print("Вы не смогли избежать ловушки... Игра окончена!")
                game_state["game_over"] = True
            else:
                print("Вам удалось избежать ловушки. Вы уцелели!")

    else:
        seed = game_state.get("steps", 0)

        random_value = pseudo_random(seed, TRAP_MODULO)

        if random_value < TRAP_DAMAGE_THRESHOLD:
            print("Вы не смогли избежать ловушки... Игра окончена!")
            game_state["game_over"] = True
        else:
            print("Вам удалось избежать ловушки. Вы уцелели!")


def random_event(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """

    seed = game_state.get("steps", 0)
    current_room = game_state["current_room"]

    seed = seed + len(game_state.get("player_inventory", [])) * 100

    event_occurs = pseudo_random(seed, 8) == 0

    if not event_occurs:
        return

    event_type = pseudo_random(seed + 1, 4)

    if event_type == 0:
        print("Вы заметили на полу блестящую монетку!")

        if current_room in ROOMS:
            room_items = ROOMS[current_room].get("items", [])
            if "coin" not in room_items:
                room_items.append("coin")
                ROOMS[current_room]["items"] = room_items

    elif event_type == 1:
        print("Вы услышали подозрительный шорох...")

        if "sword" in game_state["player_inventory"]:
            print("Вы хватаетесь за меч, и шорох прекращается.")
            print(" Вы отпугнули неизвестное существо!")
        else:
            print("Вам становится не по себе...")
    elif event_type == 2:
        if (
            current_room == "trap_room"
            and "torch" not in game_state["player_inventory"]
        ):
            print("Вы чувствуете опасность...")
            trigger_trap(game_state)


def pseudo_random(seed, modulo):
    """
    Args:
        seed (int): Исходное число для генерации
        modulo (int): Верхняя граница диапазона
    Returns:
        int: Псевдослучайное целое число
    """
    seed = abs(seed) if seed < 0 else seed

    value1 = math.sin(seed * 12.9898 + 78.233) * 43758.5453
    value2 = math.cos(seed * 4.14159 + 2.71828) * 10000

    combined = abs(value1 + value2)

    fractional = combined - math.floor(combined)

    result = fractional * modulo

    return int(math.floor(result)) % modulo


def show_help(commands):
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} {desc}")
    print()
