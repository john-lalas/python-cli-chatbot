"""
##############################
## python-cli-chatbot
##
## module: agent
##
##############################
"""

import json
import logging
import requests
from utils.constants import API, ApiRecord
from conversation.conversation import get_convo


def post_request(api: ApiRecord, payload: dict) -> requests.Response | None:
    """
    Create API request. Returns None if the request fails.
    """
    try:
        if api.api == API.OLLAMA:
            logging.info("Sending to url: %s", api.api_url)
            logging.info("Sending to model: %s", api.api_model)
            logging.info("Sending to key: %s", api.api_key)
            return requests.post(url=api.api_url, json=payload, stream=False, timeout=60)

        return requests.post(url=api.api_url, headers=api.headers, json=payload, timeout=60)
    except requests.exceptions.RequestException as e:
        logging.error("Request to %s failed: %s", api.api_url, e)
        return None


def handle_response(api: API, response: requests.Response | None):
    """
    Handle HTTP response
    """
    if response is None:
        return None

    ai_dict: dict = {
        API.OPEN_AI: handle_openai_result,
        API.CLAUDE: handle_claude_result,
        API.OLLAMA: handle_ollama_result,
    }
    return ai_dict.get(api)(response)


def handle_openai_result(response: requests.Response):
    """
    Handle result from OpenAI
    """
    # Unpack response
    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        logging.info("Result: %s", result)
        logging.info("Answer: %s", answer)
    else:
        logging.error("Error response: %s", response.status_code)


def handle_claude_result(response: requests.Response):
    """
    Handle result from Claude
    """
    # Unpack response
    if response.status_code == 200:
        result = response.json()
        answer = result["content"][0]["text"]
        logging.info("Result: %s", result)
        logging.info("Answer: %s", answer)
    else:
        logging.error("Error response: %s", response.status_code)


def handle_ollama_result(response: requests.Response):
    """
    Handle result from Ollama
    """
    # Unpack response
    if response.status_code == 200:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                json_line = json.loads(decoded_line)
                message = json_line.get("message", "")
                content = message.get("content", "")
                print(content)
                print("\n")
                get_convo().save_response(response=content)
    else:
        logging.error("Error response: %s", response.status_code)
