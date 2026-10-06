"""
##############################
## python-cli-chatbot
##############################
"""

import logging
from agent.agent import Agent, get_agent
from menu.main_menu import MainMenu
from prompt.prompt import get_prompt, Prompt
from utils.stop import get_stop


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

    get_stop().clear()
    prompt: Prompt = get_prompt()

    agent: Agent = get_agent()
    while not get_stop().stopped:
        p: str = prompt.prompt()
        if p and len(p) > 0:
            agent.infer(prompt=p, context=prompt.context)


if "main" in __name__:
    main()
