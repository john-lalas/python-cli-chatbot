"""
##############################
## python-cli-chatbot
##############################
"""

import logging
from dotenv import load_dotenv
from agent.agent import Agent, get_agent
from menu.main_menu import MainMenu
from prompt.prompt import prompt
from utils.stop import get_stop


def initialize():
    """
    Initialize python-cli-chatbot
    """
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Load dot environment files
    load_dotenv()


def main() -> None:
    """
    Main entry point
    """
    initialize()

    menu: MainMenu = MainMenu()
    while not get_stop().stopped:
        menu.show()

    get_stop().clear()

    agent: Agent = get_agent()
    while not get_stop().stopped:
        p: str = prompt()
        if "quit" in p.lower():
            get_stop().stop()
            break

        if p and len(p) > 0:
            agent.infer(prompt=p)


if "main" in __name__:
    main()
