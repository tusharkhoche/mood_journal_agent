from state import JournalState
from nodes import analyze_mood


def make_state(entry_text: str) -> JournalState:
    # Minimal state for testing this node
    return {
        "entry_text": entry_text,
        "sentiment": None,
        "tags": None,
        "reflection": None,
        "history": None,
    }


def run_test(entry_text: str):
    state = make_state(entry_text)
    result = analyze_mood(state)
    print(f"ENTRY: {entry_text!r}")
    print(f"RESULT: {result}")
    print("-" * 60)


if __name__ == "__main__":
    run_test("Had a great day, finished my tasks and enjoyed dinner with friends.")
    #run_test("Feeling exhausted and stressed. Too many meetings and I didn't finish my work.")
    #run_test("Today was okay. Nothing special happened, just went through the routine.")
    #run_test("")  # empty input edge case
