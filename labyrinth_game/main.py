

"""
Главный файл игры Лабиринт
"""

# Импортируем созданные модули и переменные
from labyrinth_game.player_actions import show_inventory, move_player, use_item, take_item, get_input
from labyrinth_game.utils import describe_current_room, solve_puzzle, attempt_open_treasure, show_help
from labyrinth_game.constants import ROOMS, COMMANDS

# Функция обработки команды пользователя
def process_command(game_state, command):
    """
    Args:
        game_state (dict): Состояние игры
        command (str): Введенная пользователем команда
    """
    # Разделяем команду на части
    parts = command.strip().split()
    if not parts:  # Пустая команда
        return

    # Первое слово - команда, остальное - аргумент
    cmd = parts[0].lower()
    arg = ' '.join(parts[1:]) if len(parts) > 1 else None

    # Используем match/case для определения команды
    match cmd:
        case "look":
            describe_current_room(game_state)

        case "use":
            if arg:
                use_item(arg, game_state)
            else:
                print("Укажите предмет для использования.")

        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление.")

        # Односложные команды движения без "go"
        case "north" | "south" | "east" | "west":
            from labyrinth_game.player_actions import move_player
            move_player(game_state, cmd)

        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет для взятия.")

        case "inventory":
            show_inventory(game_state)

        case "solve":
            if game_state['current_room'] == 'treasure_room':
                from labyrinth_game.utils import attempt_open_treasure
                attempt_open_treasure(game_state)
            else:
                from labyrinth_game.utils import solve_puzzle
                solve_puzzle(game_state)

        case "help":
            show_help(COMMANDS)

        case "quit" | "exit" | "выход":
            print("Выход из игры.")
            game_state['game_over'] = True

        case _:
            print(f"Неизвестная команда: {cmd}")

# Основной игровой цикл
def main():

# Определяем состояние игрока
    game_state = {
      'player_inventory': [], # Инвентарь игрока
      'current_room': 'entrance', # Текущая комната
      'game_over': False, # Значения окончания игры
      'steps_taken': 0 # Количество шагов
}

# Выводим приветственное сообщение
    print("Добро пожаловать в Лабиринт сокровищ!")

# Вызываем функцию, описывающую стартовую комнату
    describe_current_room(game_state)

    # Цикл while, который будет работать, пока игра не окончена
    while not game_state['game_over']:
        # Считываем команду от пользователя
        command = get_input("> ")

        # Обрабатываем команду
        process_command(game_state, command)

        # Обработка команды выхода
        if command == "выход":
            game_state['game_over'] = True
            print("Спасибо за игру!")
        else:
            # Выводим введенную команду
            print(f"Вы ввели: {command}")

 if __name__ == "__main__":
    main()
