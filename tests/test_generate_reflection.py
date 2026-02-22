from state import JournalState
from nodes import analyze_mood, extract_tags, generate_reflection


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

        mood_update = analyze_mood(state)
        state.update(mood_update)

        tags_update = extract_tags(state)
        state.update(tags_update)

        reflection_update = generate_reflection(state)
        state.update(reflection_update)

        print("ENTRY:", repr(t))
        print("SENTIMENT:", state["sentiment"])
        print("TAGS:", state["tags"])
        print("Reflection:", state["reflection"])
        print("-" * 60)
