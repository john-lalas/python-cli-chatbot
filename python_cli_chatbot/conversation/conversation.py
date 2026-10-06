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


class Conversation:
    """
    Class to manage conversation between user and model.
    """

    def save_prompt(self, prompt) -> None:
        """
        Save user prompt
        """
        logging.info("Save prompt: %s", prompt)

    def save_response(self, response) -> None:
        """
        Save response from model
        """
        logging.info("Save prompt: %s", response)


@lru_cache(maxsize=1)
def get_convo():
    """
    Get Conversation singleton
    """
    return Conversation()
