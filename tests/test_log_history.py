from state import JournalState
from nodes import log_history

state: JournalState = {
    "entry_text": "dummy",
    "sentiment": None,
    "tags": None,
    "reflection": None,
    "history": None,
}

def add_reflection(text: str):
    state["reflection"] = text
    update = log_history(state)
    state.update(update)
    print("Added:", repr(text))
    print("History:", state["history"])
    print("-" * 40)

if __name__ == "__main__":
    add_reflection("Reflection 1")
    add_reflection("Reflection 2")
    add_reflection("Reflection 3")
