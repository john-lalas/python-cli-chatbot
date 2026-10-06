"""
##############################
## python-cli-chatbot
##
## module: agent
##
##############################
"""

from dataclasses import dataclass
import requests
from agent.agent import API


@dataclass
class ApiRecord:
    """
    Dataclass that contains data needed to make API calls.
    """

    api: API = API.UNKNOWN
    api_key: str = ""
    api_url: str = ""
    api_model: str = ""
    headers: dict = {}


def select_model(api: API) -> str:
    """
    Select model from AI
    """
    model_dict: dict = {
        "openai": "gpt-4o-mini",
        "claude": "claude-3-5-sonnet-20241022",
        "ollama": "llama3",
    }
    return model_dict.get(ai)


def empty_api_payload(ai: str, prompt: str) -> dict:
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
        return requests.post(url=api.api_url, json=payload, stream=True)

    return requests.post(url=api.api_url, headers=api.headers, json=payload)

def handle_response(ai: str, response: requests.Response):
    """
    Handle HTTP response
    """
    ai_dict: dict = {"openai": handle_openai_result, "claude": handle_claude_result}
    return ai_dict.get(ai)()


def handle_openai_result(response: requests.Response):
    """
    Handle result from OpenAI
    """
    # Unpack response
    if response.status_code == 200:
        result = response.json()
        answer = result["choices"][0]["message"]["comment"]
        logging.info(answer)
    else:
        logging.error(f"Error response: {response.status_code}")


def handle_claude_result(response: requests.Response):
    """
    Handle result from Claude
    """
    # Unpack response
    if response.status_code == 200:
        result = response.json()
        answer = result["content"][0]["text"]
        logging.info(answer)
    else:
        logging.error(f"Error response: {response.status_code}")


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
                logging.info(json_line.get("response", ""))
    else:
        logging.error(f"Error response: {response.status_code}")