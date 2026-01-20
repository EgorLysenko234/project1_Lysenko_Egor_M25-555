"""
Действия игрока в игре Лабиринт

"""
# Импортируем необходимые файлы
from labyrinth_game.constants import ROOMS
from labyrinth_game.utils import describe_current_room

# Отоброжение инвентаря игрока
def show_inventory(game_state):
    """
    Args:
        game_state (dict): Словарь состояния игры, должен содержать ключ 'player_inventory'
    """

    inventory = game_state.get('player_inventory', [])

    if inventory:
        print("Инвентарь игрока:")
        for item in inventory:
            print(f"  - {item}")
    else:
        print("Инвентарь пуст.")

# Функция перемещения в нужное направление
def move_player(game_state, direction):
    """
    Args:
        game_state (dict): Состояние игры
        direction (str): Направление движения ('north', 'south', 'west', 'east')

    Returns:
        bool: True если перемещение успешно, False если нет
    """

    current_room_name = game_state['current_room']
    current_room = ROOMS.get(current_room_name)

    if not current_room:
        print(f"Ошибка: комната "{current_room_name}" не найдена!")
        return False

    exits = current_room.get('exits', {})

    if direction in exits:

        new_room = exits[direction]

        if new_room == 'treasure_room' and 'rusty_key' not in game_state['player_inventory']:
            print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            return False
        elif new_room == 'treasure_room' and 'rusty_key' in game_state['player_inventory']:
            print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")

        # В move_player добавить проверку:
        if new_room == 'secret_room' and game_state['current_room'] == 'library':
    # Проверяем, решена ли загадка в библиотеке
            if 'library_access' not in game_state.get('solved_puzzles', []):
                print("Проход в секретную комнату закрыт. Нужно решить загадку в библиотеке.")
                return False

        game_state['current_room'] = new_room
        game_state['steps'] += 1

        direction_names = {
            'north': 'север',
            'south': 'юг',
            'west': 'запад',
            'east': 'восток'
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

# Функция использования предметов
def use_item(game_state, item_name):
    """
    Использовать предмет из инвентаря.

    Args:
        game_state (dict): Состояние игры
        item_name (str): Название предмета для использования
    """

    if item_name not in game_state['player_inventory']:
        print(f"У вас нет такого предмета.")
        return


    if item_name == "torch":
        print("Стало светлее.")

    elif item_name == "sword":
        print("Вы чувствуете уверенность, держа меч в руках.")

    elif item_name == "ancient_scroll":
        print("Вы читаете древний свиток: 'Код сокровищницы: 4857'")
        if 'treasure_code' not in game_state:
            game_state['treasure_code'] = '4857'

    elif item_name == "flower_key":
        if game_state['current_room'] == 'hall':
            print("Вы вставляете цветочный ключ в золотую дверь...")
            print("Дверь открывается! Вы нашли выход из лабиринта!")
            game_state['game_over'] = True
        else:
            print("Здесь нет подходящей двери для этого ключа.")
    
    elif item_name == "throne":
        if game_state['current_room'] == 'hall':
            print("Вы садитесь на трон. Чувствуете себя королем!")
            print("Это придает вам уверенности.")
        else:
            print("Здесь нет трона.")

    elif item_name == "bronze_box":
        print("Вы открыли бронзовую шкатулку.")

        if "rusty_key" not in game_state['player_inventory']:
            game_state['player_inventory'].append("rusty_key")
            print("Вы нашли серебрянный ключ!")

    else:
        print("Вы не знаете, как использовать этот предмет.")

# Функция взятия предметов
def take_item(game_state, item_name):
    """
    Args:
        game_state (dict): Состояние игры
        item_name (str): Название предмета для взятия
    """
    current_room_name = game_state['current_room']


    if current_room_name not in ROOMS:
        print("Ошибка: текущая комната не найдена!")
        return

    current_room = ROOMS[current_room_name]
    items_in_room = current_room.get('items', [])

    if item_name == 'treasure_chest':
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return

    if item_name in items_in_room:

        game_state['player_inventory'].append(item_name)


        items_in_room.remove(item_name)


        print(f"Вы подняли {item_name}.")
    else:
        print("Такого предмета здесь нет.")

# Вывод от пользователя
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
