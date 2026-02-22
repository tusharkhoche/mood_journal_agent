from state import JournalState
from nodes import extract_tags


def make_state(entry_text: str) -> JournalState:
    return {
        "entry_text": entry_text,
        "sentiment": None,
        "tags": None,
        "reflection": None,
        "history": None,
    }


if __name__ == "__main__":
    texts = [
        "Had a busy day at work, lots of meetings but I felt productive.",
        "Spent time with family and went for a walk in the park. Felt calm.",
        "Feeling burned out and stressed, not sleeping well, too many deadlines.",
    ]

    for t in texts:
        state = make_state(t)
        result = extract_tags(state)
        print("ENTRY:", repr(t))
        print("TAGS: ", result["tags"])
        print("-" * 60)
