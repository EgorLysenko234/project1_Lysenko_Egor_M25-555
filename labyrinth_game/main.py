"""
Главный файл игры Лабиринт
"""

from labyrinth_game.constants import COMMANDS
from labyrinth_game.player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)
from labyrinth_game.utils import describe_current_room, show_help


def process_command(game_state, command):
    """
    Args:
        game_state (dict): Состояние игры
        command (str): Введенная пользователем команда
    """
    parts = command.strip().split()
    if not parts:
        return

    cmd = parts[0].lower()
    arg = " ".join(parts[1:]) if len(parts) > 1 else None

    match cmd:
        case "look":
            describe_current_room(game_state)

        case "use":
            if arg:
                use_item(game_state, arg)
            else:
                print("Укажите предмет для использования.")

        case "go":
            if arg:
                move_player(game_state, arg)
            else:
                print("Укажите направление.")

        case "north" | "south" | "east" | "west":
            move_player(game_state, cmd)

        case "take":
            if arg:
                take_item(game_state, arg)
            else:
                print("Укажите предмет для взятия.")

        case "inventory":
            show_inventory(game_state)

        case "solve":
            if game_state["current_room"] == "treasure_room":
                from labyrinth_game.utils import attempt_open_treasure

                attempt_open_treasure(game_state)
            else:
                from labyrinth_game.utils import solve_puzzle

                solve_puzzle(game_state)

        case "help":
            show_help(COMMANDS)

        case "quit" | "exit" | "выход":
            print("Выход из игры.")
            game_state["game_over"] = True

        case _:
            print(f"Неизвестная команда: {cmd}")


def main():
    game_state = {
        "player_inventory": [],
        "current_room": "entrance",
        "game_over": False,
        "steps": 0,
        "solved_puzzles": [],
    }

    print("Добро пожаловать в Лабиринт сокровищ!")

    print("\nЧтобы начать, ознакомьтесь с доступными командами:")
    show_help(COMMANDS)
    print("\nДля продолжения введите команду (например, 'look' для осмотра комнаты).")
    print("-" * 50)

    describe_current_room(game_state)

    while not game_state["game_over"]:
        command = get_input("> ")

        process_command(game_state, command)

if __name__ == "__main__":
    main()
