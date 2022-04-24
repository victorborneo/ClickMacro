import os
import time
import pickle

import pyautogui
import keyboard


def get_new_macro(macros: dict) -> None:
    print(
        "Move the cursor to the position and press Enter "
        "(Press any other key to cancel)"
    )

    key = keyboard.read_key()
    if key != 'enter':
        print("Cancelling.")
        return

    x, y = pyautogui.position()

    print(
        "What's the bind button? "
        "(Can't be Insert, Pause, Enter, Delete or End)"
    )
    while key in ('delete', 'insert', 'pause', 'enter', 'end'):
        key = keyboard.read_key()
    bind = key
    print(f"Bind button: {bind}")

    print("Return to original position after click? (y/n)")
    while key not in ('y', 'n'):
        key = keyboard.read_key()

    if key == 'y':
        macros[bind] = (x, y, True)
    else:
        macros[bind] = (x, y, False)
    print("Macro created successfully.")


def delete_macro(macros: dict) -> None:
    if not len(macros):
        print("No macros.")
        return

    for key, value in macros.items():
        print(f"{key} -> {value}")

    print(
        "Press the bind button to be deleted. "
        "If it doesn't exist the operation will cancel."
    )

    key = keyboard.read_key()

    if macros.get(key) is not None:
        del macros[key]
        print(f"Macro {key} deleted successfully.")
        return
    print(f"No macros with bind {key}. Cancelling.")


def macro(*args) -> None:
    x, y, back = args[0], args[1], args[2]
    cur_x, cur_y = pyautogui.position()

    pyautogui.click(x, y)

    if back:
        pyautogui.moveTo(cur_x, cur_y)


def clear():
    os.system('cls || clear')
    print(
        "Press End to stop.\n"
        "Press Insert to create a macro.\n"
        "Preess Delete to delete a macro.\n"
        "Press Pause/Break to stop/resume the "
        "program from receiving inputs."
    )


def load_macros() -> dict:
    if os.path.exists("macros.pickle"):
        with open("macros.pickle", "rb") as content:
            return pickle.load(content)
    return {}


def save_macros(macros: dict) -> None:
    with open("macros.pickle", "wb") as content:
        pickle.dump(macros, content)


def main():
    key = None
    paused = False
    macros = load_macros()

    clear()
    while key != 'end':
        if key in ('pause', 'insert', 'delete'):
            time.sleep(0.1)
            if key == 'pause':
                paused = not paused
                print("Paused") if paused else clear()
            elif not paused:
                clear()
                get_new_macro(macros) if key == 'insert' else delete_macro(macros)
                save_macros(macros)
        elif not paused and macros.get(key) is not None:
            macro(*macros[key])

        key = keyboard.read_key()


if __name__ == "__main__":
    main()
