"""
##############################
## python-cli-chatbot
##
## module: conversation
##
##############################
"""

import json
import logging
from functools import lru_cache
from pathlib import Path
from utils.constants import HISTORY_FILE, MAX_HISTORY_EXCHANGES


class Conversation:
    """
    Class to manage conversation between user and model.
    History is loaded from history_file on creation and written back on every save.
    Pass history_file=None to keep history in memory only.
    """

    def __init__(self, history_file: Path | None = HISTORY_FILE):
        self._history_file: Path | None = history_file
        self._messages: list[dict] = self._load()

    def _load(self) -> list[dict]:
        """
        Load history from file. A missing file starts an empty history; an
        unreadable one is moved aside to <name>.bak so it isn't overwritten.
        """
        if self._history_file is None or not self._history_file.exists():
            return []

        try:
            data = json.loads(self._history_file.read_text(encoding="utf-8"))
            if not isinstance(data, list) or not all(
                isinstance(m, dict)
                and m.get("role") in ("user", "assistant")
                and isinstance(m.get("content"), str)
                for m in data
            ):
                raise ValueError("expected a list of role/content messages")
        except (OSError, ValueError) as e:
            backup: Path = self._history_file.with_suffix(".json.bak")
            logging.warning(
                "Could not load history from %s (%s); moving it to %s",
                self._history_file,
                e,
                backup,
            )
            try:
                self._history_file.replace(backup)
            except OSError as move_error:
                logging.error("Could not move %s: %s", self._history_file, move_error)
            return []

        logging.debug("Loaded %d messages from %s", len(data), self._history_file)
        return [{"role": m["role"], "content": m["content"]} for m in data]

    def _save(self) -> None:
        """
        Write history to file, via a temp file so a crash can't leave it half written
        """
        if self._history_file is None:
            return

        try:
            self._history_file.parent.mkdir(parents=True, exist_ok=True)
            tmp: Path = self._history_file.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(self._messages, indent=2), encoding="utf-8")
            tmp.replace(self._history_file)
        except OSError as e:
            logging.error("Could not save history to %s: %s", self._history_file, e)

    def save_prompt(self, prompt: str) -> None:
        """
        Save user prompt
        """
        logging.debug("Save prompt: %s", prompt)
        self._messages.append({"role": "user", "content": prompt})
        self._save()

    def save_response(self, response: str) -> None:
        """
        Save response from model
        """
        logging.debug("Save response: %s", response)
        self._messages.append({"role": "assistant", "content": response})
        self._save()

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
