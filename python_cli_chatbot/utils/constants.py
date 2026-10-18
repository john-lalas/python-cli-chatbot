"""
##############################
## python-cli-chatbot
##
## module: utils
##
##############################
"""

from enum import Enum
from dataclasses import dataclass, field

# Number of past prompt/response pairs sent with each request
MAX_HISTORY_EXCHANGES: int = 10


class API(Enum):
    """
    Enumeration for AI agent types
    """

    UNKNOWN = 0
    CLAUDE = 1
    OLLAMA = 2
    OPEN_AI = 3


@dataclass
class ApiRecord:
    """
    Dataclass that contains data needed to make API calls.
    """

    api: API = API.UNKNOWN
    api_key: str = ""
    api_url: str = ""
    api_model: str = ""
    headers: dict = field(default_factory=dict)
