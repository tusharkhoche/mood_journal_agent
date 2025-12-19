import json
from pathlib import Path


HISTORY_FILE = Path("history.json")


def load_history():
    """
    Load history list from history.json.
    Returns an empty list if file does not exist or data is invalid.
    """

    # If file does not exist, return empty history
    if not HISTORY_FILE.exists():
        return []

    try:
        text = HISTORY_FILE.read_text(encoding="utf-8")
        data = json.loads(text)

        history = data.get("history")

        # Validate history is a list of strings
        if isinstance(history, list):
            cleaned = []
            for item in history:
                if isinstance(item, str):
                    cleaned.append(item)
            return cleaned

    except json.JSONDecodeError as e:
        print("Error parsing history.json (invalid JSON):")
        print(e)


    except UnicodeDecodeError as e:
        print("Error reading history.json (encoding issue):")
        print(e)


    except OSError as e:
    # Covers file read issues (permissions, IO errors, etc.)
       print("File system error while reading history.json:")
       print(e)

    return []


def save_history(history):
    """
    Save history list to history.json.
    """

    payload = {}
    payload["history"] = history

    json_text = json.dumps(payload, ensure_ascii=False, indent=2)
    HISTORY_FILE.write_text(json_text, encoding="utf-8")
