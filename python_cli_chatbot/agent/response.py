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


def empty_api_payload(_: str, __: str) -> dict:
    """
    Empty payload
    """
    return {}


def create_api_payload(api: API, prompt: str) -> dict:
    """
    Make API payload that contains prompt
    """
    model_dict: dict = {
        API.OPEN_AI: create_openai_payload,
        API.CLAUDE: create_claude_payload,
        API.OLLAMA: create_ollama_payload,
    }
    return model_dict.get(api, empty_api_payload)(api.api_model, prompt)


def create_openai_payload(model: str, prompt: str) -> dict:
    """
    Make API payload that contains prompt
    """
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a concise assistant."},
            {"role": "user", "content": f"{prompt}"},
        ],
        "temperature": 0.7,
    }


def create_claude_payload(model: str, prompt: str) -> dict:
    """
    Make API payload that contains prompt
    """
    return {
        "model": model,
        "max_tokens": 1024,
        "messages": [
            {"role": "user", "content": f"{prompt}"},
        ],
    }


def create_ollama_payload(model: str, prompt: str) -> dict:
    """
    Make API payload that contains prompt
    """
    return {"model": model, "prompt": prompt, "stream": True}


def post_request(api: ApiRecord, payload: dict) -> requests.Response:
    """
    Create API request
    """
    if api.api == API.OLLAMA:
        logging.info("Sending to url: %s", api.api_url)
        logging.info("Sending to model: %s", api.api_model)
        logging.info("Sending to key: %s", api.api_key)
        return requests.post(url=api.api_url, json=payload, stream=False)

    return requests.post(url=api.api_url, headers=api.headers, json=payload, timeout=60)


def handle_response(api: API, response: requests.Response):
    """
    Handle HTTP response
    """
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
        answer = result["choices"][0]["message"]["comment"]
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
                logging.info("Response: %s", json_line)
                # logging.info("Response: %s", json_line.get("response", ""))
    else:
        logging.error("Error response: %s", response.status_code)
