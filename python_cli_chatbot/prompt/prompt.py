"""
##############################
## python-cli-chatbot
##
## module: prompt
##
##############################
"""

from functools import lru_cache
from utils.stop import Stop, get_stop


class Prompt:
    """
    Prompt class that contains all prompts that are contained in
    the context for this session.
    """

    def __init__(self):
        self._context: list = []
        self._stop: Stop = get_stop()

    def prompt(self) -> str:
        """
        Obtain prompt from user.  Store in local context.
        """
        p: str = input("Prompt: ")
        if "quit" in p.lower():
            self._stop.stop()
            p = ""
        if p and len(p) > 0:
            self._context.append(p)
        return p

    @property
    def context(self):
        """
        Return context property
        """
        return self._context


@lru_cache(maxsize=1)
def get_prompt():
    """
    Return singleton Prompt
    """
    return Prompt()
