"""
##############################
## python-cli-chatbot
##
## module: menu
##
##############################
"""

from utils.stop import get_stop
from agent.agent import get_agent, Agent, Model


class MainMenu:
    """
    Class that creates CLI menu.
    """

    def __init__(self):
        self._agent: Agent = get_agent()

    def handle_ollama(self):
        """
        Handle Ollama API
        """
        self._agent.change(model=Model.OLLAMA)
        get_stop().stop()

    def handle_claude(self):
        """
        Handle Claude Code API
        """
        self._agent.change(model=Model.CLAUDE)
        get_stop().stop()

    def handle_open_ai(self):
        """
        Handle OpenAI API
        """
        self._agent.change(model=Model.OPEN_AI)
        get_stop().stop()

    def handle_quit(self):
        """
        Handle quit
        """
        get_stop().stop()

    def handle_unknown(self):
        """
        Handle unknown
        """
        print("Unknown choice")

    def show(self):
        """
        Start Menu
        """
        choice_dict: dict = {
            "1": self.handle_ollama,
            "2": self.handle_claude,
            "3": self.handle_open_ai,
            "q": self.handle_quit,
        }
        print("=== Choose AI API ===")
        print("1. Ollama")
        print("2. Claude Code")
        print("3. OpenAI")
        print("Q/q. Quit")
        print("================")

        choice: str = input("Enter your choice (1-3 or Q/q): ").strip().lower()
        choice_dict.get(choice, self.handle_unknown)()
