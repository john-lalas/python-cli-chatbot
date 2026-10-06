"""
##############################
## python-cli-chatbot
##
## module: agent
##
##############################
"""

import logging
from enum import Enum
from functools import lru_cache
from conversation.conversation import Conversation, get_convo


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
        self._convo: Conversation = get_convo()

    def change(self, model: Model) -> None:
        """
        Change model
        """
        self._model = model

    def infer(self, prompt: str) -> None:
        """
        Make inference from prompt.
        """
        logging.info("Make inference: %s", prompt)
        self._convo.save_prompt(prompt=prompt)

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
