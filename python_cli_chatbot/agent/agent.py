"""
##############################
## python-cli-chatbot
##
## module: agent
##
##############################
"""

import os
import logging
from enum import Enum
from functools import lru_cache
import requests
from conversation.conversation import Conversation, get_convo
from response import ApiRecord, post_request


class API(Enum):
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
        self._api: ApiRecord = ApiRecord()
        self._convo: Conversation = get_convo()

    def create_payload(self, api: API, prompt: str) -> dict:
        """
        Create API payload
        """
        payload_dict: dict = {
            API.CLAUDE: {
                "model": api.api_model,
                "max_tokens": 1024,
                "messages": [
                    {"role": "user", "content": f"{prompt}"},
                ],
            },
            API.OLLAMA: {"model": api.api_model, "prompt": prompt, "stream": True},
            API.OPEN_AI: {
                "model": api.api_model,
                "messages": [
                    {"role": "system", "content": "You are a concise assistant."},
                    {"role": "user", "content": f"{prompt}"},
                ],
                "temperature": 0.7,
            },
        }
        return payload_dict.get(api, {})

    def setup_claude(self) -> None:
        """
        Setup Claude API
        """
        api_key: str = os.environ.get("ANTHROPIC_API_KEY")
        self._api = ApiRecord(
            api=API.CLAUDE,
            api_key=api_key,
            api_url=os.environ.get("ANTHROPIC_API_URL"),
            api_model="claude-3-5-sonnet-20241022",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
        )

    def setup_ollama(self) -> None:
        """
        Setup Claude API
        """
        api_key: str = os.environ.get("OLLAMA_API_KEY")
        self._api = ApiRecord(
            api=API.OLLAMA,
            api_key=api_key,
            api_url=os.environ.get("OLLAMA_API_URL"),
            api_model="llama3",
            headers={},
        )

    def setup_openai(self) -> None:
        """
        Setup OpenAI
        """
        api_key: str = os.environ.get("OPENAI_API_KEY")
        self._api = ApiRecord(
            api=API.OPEN_AI,
            api_key=api_key,
            api_url=os.environ.get("OPENAI_API_URL"),
            api_model="gpt-4o-mini",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )

    def unknown_api(self) -> None:
        """
        Unknown AI
        """
        logging.error("Unknown AI specified")
        self._api = ApiRecord(
            api=API.UNKNOWN,
            api_key="UNKNOWN",
            api_url="UNKNOWN",
            headers={
                "Content-Type": "application/json",
                "Authorization": "UNKNOWN",
            },
        )

    def change(self, api: API) -> None:
        """
        Change model
        """
        api_dict: dict = {
            API.OPEN_AI: self.setup_openai,
            API.OLLAMA: self.setup_ollama,
            API.CLAUDE: self.setup_claude,
        }
        api_dict.get(api, self.unknown_api)()

    def infer(self, prompt: str) -> None:
        """
        Make inference from prompt.
        """
        logging.info("Make inference: %s", prompt)
        self._convo.save_prompt(prompt=prompt)
        payload: dict = self.create_payload(api=self._api)
        response: requests.Response = post_request(api=self._api, payload=payload)
        logging.info("Response: %s", response)

    @property
    def model(self) -> API:
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
