from ui.core import ready_shell_ui
from sandbosh import welcome_message


def main() -> None:
    welcome_message()

    # UIの表示
    ready_shell_ui()


if __name__ == "__main__":
    main()
