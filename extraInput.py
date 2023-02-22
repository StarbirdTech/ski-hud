import keyboard


def multipleChoice(options):
    selected = 0
    done = False

    # enter application mode
    print("\033[?1049h", end="")

    while not done:
        print("\033c", end="")
        for i in range(len(options)):
            if i == selected:
                print(">", end="")
            else:
                print(" ", end="")
            print(options[i])

        key = keyboard.read_key()
        if key == "up":
            selected -= 1
        elif key == "down":
            selected += 1
        elif key == "enter":
            done = True
        elif key == "escape":
            exit()

        if selected < 0:
            selected = len(options) - 1
        elif selected >= len(options):
            selected = 0

        # wait until key is released
        while keyboard.is_pressed(key):
            pass

    return selected


if __name__ == "__main__":
    print(f'Selected Array Index: {multipleChoice(["test1", "test2", "test3", "test4", "test5"])}')
