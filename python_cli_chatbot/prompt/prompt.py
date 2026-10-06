"""
##############################
## python-cli-chatbot
##
## module: prompt
##
##############################
"""

from utils.stop import get_stop


def prompt() -> str:
    """
    Obtain prompt from user.  Store in local context.
    """
    p: str = input("Prompt: ")
    if "quit" in p.lower():
        get_stop.stop()
        p = ""
    return p
