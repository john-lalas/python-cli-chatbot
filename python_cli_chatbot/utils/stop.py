"""
##############################
## python-cli-chatbot
##
## module: utils
##
##############################
"""

from functools import lru_cache


class Stop:
    """
    Class to indicate stop
    """

    def __init__(self):
        self._stop: bool = False

    def stop(self):
        """
        Set stop
        """
        self._stop = True

    def clear(self):
        """
        Clear stop
        """
        self._stop = False

    @property
    def stopped(self) -> bool:
        """
        Return property
        """
        return self._stop


@lru_cache(maxsize=1)
def get_stop():
    """
    Return Stop singleton
    """
    return Stop()
