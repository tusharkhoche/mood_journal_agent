from graph import build_graph
from state import JournalState
from storage import save_history, load_history

def initialize_state(entry_text: str) -> JournalState:
    memory = load_history()

    return {
        "entry_text": entry_text,
        "sentiment": None,
        "tags": None,
        "reflection": None,
        "history": memory,
    }


if __name__ == "__main__":
    graph = build_graph()
    entry = input("How was your day? ").strip()

    state = initialize_state(entry)
    final_state = graph.invoke(state)

    print("\n--- Results ---")
    print("Sentiment:", final_state["sentiment"])
    print("Tags:", final_state["tags"])
    print("Reflection:", final_state["reflection"])
    save_history(final_state["reflection"])
    #print("History:", final_state["history"])
