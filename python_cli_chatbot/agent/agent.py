"""
##############################
## python-cli-chatbot
##
## module: agent
##
##############################
"""

from enum import Enum
from functools import lru_cache


class Model(Enum):
    """
    Enumeration for AI agent types
    """

    UNKNOWN = 0
    CLAUDE = 1
    OLLAMA = 2
    OPEN_AI = 3


class Agent:
    """
    Class keeps track of AI agent
    """

    def __init__(self):
        self._model: Model = Model.UNKNOWN

    def change(self, model: Model) -> None:
        """
        Change model
        """
        self._model = model

    @property
    def model(self) -> Model:
        """
        Model property
        """
        return self._model


@lru_cache(maxsize=1)
def get_agent():
    """
    Get the Agent singleton
    """
    return Agent()
