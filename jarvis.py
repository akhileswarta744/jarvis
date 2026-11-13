"""Minimal JARVIS voice-dictation + local Ollama chat starter.

OpenWhispr supplies speech-to-text by dictating into this terminal's prompt.
This program sends text only to the local Ollama HTTP API.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_dotenv() -> None:
    """Load simple KEY=VALUE settings from .env without an extra dependency."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for raw_line in env_file.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("\"'")
        if key:
            os.environ.setdefault(key, value)


def ask_ollama(messages: list[dict[str, str]]) -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434").rstrip("/")
    model = os.getenv("OLLAMA_MODEL", "qwen3.5:2b")
    timeout = float(os.getenv("OLLAMA_TIMEOUT_SECONDS", "120"))
    body = json.dumps({"model": model, "messages": messages, "stream": False}).encode("utf-8")
    request = urllib.request.Request(
        f"{base_url}/api/chat",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        details = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Ollama returned HTTP {exc.code}: {details}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "Could not reach Ollama. Open the Ollama app and check OLLAMA_BASE_URL."
        ) from exc
    except TimeoutError as exc:
        raise RuntimeError("Ollama did not respond before the configured timeout.") from exc

    answer = result.get("message", {}).get("content", "").strip()
    if not answer:
        raise RuntimeError("Ollama returned an empty response. Check that the model is installed.")
    return answer


def main() -> int:
    load_dotenv()
    model = os.getenv("OLLAMA_MODEL", "qwen3.5:2b")
    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are JARVIS, a concise and helpful personal assistant. "
                "You can answer questions and help with planning. You cannot control "
                "the computer or perform actions; say so clearly when asked."
            ),
        }
    ]
    print("JARVIS — local assistant starter")
    print(f"Model: {model}")
    print("Type a message, dictate into the prompt with OpenWhispr, /reset for a new chat, or /quit to exit.")

    while True:
        try:
            text = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            return 0
        if not text:
            continue
        command = text.casefold()
        if command in {"/quit", "/exit"}:
            print("Goodbye.")
            return 0
        if command == "/reset":
            messages = messages[:1]
            print("Conversation cleared.")
            continue

        pending = messages + [{"role": "user", "content": text}]
        try:
            answer = ask_ollama(pending)
        except (RuntimeError, ValueError, json.JSONDecodeError) as exc:
            print(f"\nJARVIS setup error: {exc}", file=sys.stderr)
            continue
        messages = pending + [{"role": "assistant", "content": answer}]
        print(f"\nJARVIS: {answer}")


if __name__ == "__main__":
    raise SystemExit(main())
