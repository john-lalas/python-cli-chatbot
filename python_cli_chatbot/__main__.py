"""
##############################
## python-cli-chatbot
##############################
"""

import logging
from python_cli_chatbot.menu.main_menu import MainMenu
from python_cli_chatbot.utils.stop import get_stop


def initialize():
    """
    Initialize python-cli-chatbot
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    """
    Main entry point
    """
    initialize()

    menu: MainMenu = MainMenu()
    while not get_stop().stopped:
        menu.show()


if "main" in __name__:
    main()
