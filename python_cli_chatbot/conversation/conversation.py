"""
##############################
## python-cli-chatbot
##
## module: conversation
##
##############################
"""

import logging
from functools import lru_cache
from utils.constants import MAX_HISTORY_EXCHANGES


class Conversation:
    """
    Class to manage conversation between user and model.
    """

    def __init__(self):
        self._messages: list[dict] = []

    def save_prompt(self, prompt: str) -> None:
        """
        Save user prompt
        """
        logging.debug("Save prompt: %s", prompt)
        self._messages.append({"role": "user", "content": prompt})

    def save_response(self, response: str) -> None:
        """
        Save response from model
        """
        logging.debug("Save response: %s", response)
        self._messages.append({"role": "assistant", "content": response})

    @property
    def messages(self) -> list[dict]:
        """
        Return all prompts and responses in order
        """
        return list(self._messages)

    def history(self, max_exchanges: int = MAX_HISTORY_EXCHANGES) -> list[dict]:
        """
        Return the last max_exchanges completed prompt/response pairs in order,
        skipping prompts that never got a response (e.g. a failed request)
        """
        if max_exchanges <= 0:
            return []

        history: list[dict] = []
        for prev, curr in zip(self._messages, self._messages[1:]):
            if prev["role"] == "user" and curr["role"] == "assistant":
                history.extend([dict(prev), dict(curr)])
        return history[-2 * max_exchanges :]

    @property
    def prompts(self) -> list[str]:
        """
        Return saved prompts
        """
        return [m["content"] for m in self._messages if m["role"] == "user"]

    @property
    def responses(self) -> list[str]:
        """
        Return saved responses
        """
        return [m["content"] for m in self._messages if m["role"] == "assistant"]


@lru_cache(maxsize=1)
def get_convo():
    """
    Get Conversation singleton
    """
    return Conversation()
