"""
Вспомогательные функции для игры Лабиринт
"""

# Импортируем константы
import math
from labyrinth_game.constants import ROOMS


# Выводим полное описание текущей комнаты
def describe_current_room(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """
    current_room_name = game_state.get('current_room', 'entrance')


    if current_room_name not in ROOMS:
        print(f"Ошибка: комната '{current_room_name}' не найдена.")
        return

    room = ROOMS[current_room_name]


    print(f"== {current_room_name.upper()} ==")
    print()


    print(room['description'])
    print()


    if room['items']:
        print("Заметные предметы:")
        for item in room['items']:
            print(f"  - {item}")
        print()


    if room['exits']:
        print("Выходы:")
        for direction, target_room in room['exits'].items():
            print(f"  {direction} -> {target_room}")
        print()

    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")
        print()

# Функция решения загадок
def solve_puzzle(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """

    current_room_name = game_state['current_room']


    if current_room_name not in ROOMS:
        print("Ошибка: текущая комната не найдена!")
        return

    current_room = ROOMS[current_room_name]


    if 'puzzle' not in current_room:
        print("Загадок здесь нет.")
        return

    puzzle_data = current_room['puzzle']

    if len(puzzle_data) == 2:
        puzzle_question, correct_answer = puzzle_data
        reward_item = 'reward'  # награда по умолчанию
    elif len(puzzle_data) == 3:
        puzzle_question, correct_answer, reward_item = puzzle_data
    else:
        print("Некорректные данные загадки.")
        return

    print(puzzle_question)


    user_answer = input("Ваш ответ: ").strip().lower()

    if correct_answer == '10' and user_answer == 'десять':
        is_correct = True
    else:
        is_correct = user_answer == correct_answer.lower()
    
    if is_correct:
        print("Верно! Загадка решена.")


        del current_room['puzzle']

        room_rewards = {
            'entrance': 'entrance_reward',
            'library': 'library_access',  # открывает доступ к secret_room
            'trap_room': 'trap_reward',
            'hall': 'victory',  # победа в игре
        }
        
        if current_room_name in room_rewards:
            reward = room_rewards[current_room_name]
            if reward == 'victory':
                print("Золотая дверь открывается! Вы победили!")
                game_state['game_over'] = True
                return
            elif reward == 'library_access':
                # Открываем проход в secret_room
                current_room['exits']['west'] = 'secret_room'
                print("Книжная полка сдвигается, открывая проход в секретную комнату!")
            else:
                game_state['player_inventory'].append(reward)
                print(f"Вы получили: {reward}")

    else:
        print("Неверно. Попробуйте снова.")

    if current_room_name == 'trap_room':
        trigger_trap(game_state)

# Функция открывания сундука
def attempt_open_treasure(game_state):
    """
    Args:
        game_state (dict): Состояние игры
    """

    current_room_name = game_state['current_room']


    if current_room_name not in ROOMS:
        print("Ошибка: текущая комната не найдена!")
        return

    current_room = ROOMS[current_room_name]


    if 'treasure_chest' not in current_room.get('items', []):
        print("Здесь нет сундука с сокровищами.")
        return


    if 'treasure_key' in game_state['player_inventory']:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")


        current_room['items'].remove('treasure_chest')

        if 'flower_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('flower_key')
            print("Вы нашли золотой ключ в виде цветка!")

        print("В сундуке сокровище!")
        return


    print("Сундук заперт. У вас нет ключа.")
    response = input("Ввести код? (да/нет): ").strip().lower()

    if response == 'да':

        if 'puzzle' not in current_room:
            print("Сундук невозможно открыть без ключа или кода.")
            return

        _, correct_code = current_room['puzzle']
        user_code = input("Введите код: ").strip()

        if user_code == correct_code:
            print("Код принят! Сундук открыт.")


            current_room['items'].remove('treasure_chest')

            if 'flower_key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('flower_key')
            print("Вы нашли золотой ключ в виде цветка (flower_key)!")

            print("В сундуке сокровище!")
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")

def trigger_trap(game_state):
    """
    Активация ловушки с негативными последствиями для игрока.
    
    Args:
        game_state (dict): Состояние игры
    """
    print("Ловушка активирована! Пол стал дрожать...")
    
    # Проверяем инвентарь игрока
    inventory = game_state['player_inventory']
    
    if inventory:  # Инвентарь не пуст
        # Используем количество шагов как seed
        seed = game_state.get('steps', 0)
        modulo = len(inventory)  # Количество предметов в инвентаре
        
        # Выбираем случайный предмет
        random_index = pseudo_random(seed, modulo)
        
        # Удаляем выбранный предмет
        lost_item = inventory.pop(random_index)
        print(f"Вы потеряли предмет: {lost_item}!")
    
    else:  # Инвентарь пуст
        seed = game_state.get('steps', 0)
        modulo = 10
        
        # Генерируем случайное число от 0 до 9
        random_value = pseudo_random(seed, modulo)
        
        if random_value < 3:  # Число меньше порога (3)
            print("Вы не смогли избежать ловушки... Игра окончена!")
            game_state['game_over'] = True
        else:
            print("Вам удалось избежать ловушки. Вы уцелели!")

def random_event(game_state):
    """
    Случайные события во время перемещения игрока.
    
    Args:
        game_state (dict): Состояние игры
    """
    
    seed = game_state.get('steps', 0)
    current_room = game_state['current_room']
    
    # Определяем, произойдет ли событие (вероятность 1/10)
    event_occurs = pseudo_random(seed, 10) == 0
    
    if not event_occurs:
        return
    
    # Выбираем тип события (0, 1 или 2)
    event_type = pseudo_random(seed + 1, 3)
    
    if event_type == 0:  # Сценарий 1: Находка
        print("Вы заметили на полу блестящую монетку!")
        
        # Добавляем монетку в текущую комнату
        if current_room in ROOMS:
            room_items = ROOMS[current_room].get('items', [])
            if 'coin' not in room_items:
                room_items.append('coin')
                ROOMS[current_room]['items'] = room_items
    
    elif event_type == 1:  # Сценарий 2: Испуг
        print("Вы услышали подозрительный шорох...")
        
        # Проверяем наличие меча
        if 'sword' in game_state['player_inventory']:
            print("Вы хватаетесь за меч, и шорох прекращается.")
            print(" Вы отпугнули неизвестное существо!")
        else:
            print("Вам становится не по себе...")
    elif event_type == 2:  # Сценарий 3: Срабатывание ловушки
        # Проверяем условия: комната trap_room и отсутствие факела
        if current_room == 'trap_room' and 'torch' not in game_state['player_inventory']:
            print("Вы чувствуете опасность...")
            trigger_trap(game_state)

# Функция псевдо рандома
def pseudo_random(seed, modulo):
    """
    Генерирует псевдослучайное число в диапазоне [0, modulo).
    
    Args:
        seed (int): Исходное число для генерации
        modulo (int): Верхняя граница диапазона
    
    Returns:
        int: Псевдослучайное целое число
    """
    seed = abs(seed) if seed < 0 else seed

    # 1. Берем синус от seed, умноженного на большое число
    value = math.sin(seed * 12.9898)
    
    # 2. Умножаем на другое большое число
    value = value * 43758.5453
    
    # 3. Получаем дробную часть
    fractional = value - math.floor(value)
    
    # 4. Приводим к диапазону [0, modulo)
    result = fractional * modulo
    
    # 5. Отбрасываем дробную часть и возвращаем целое число
    return int(math.floor(result))


# Справка (список доступных команд)
def show_help(commands):
    print("\nДоступные команды:")
    for cmd, desc in commands.items():
        print(f"  {cmd:<16} {desc}")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
