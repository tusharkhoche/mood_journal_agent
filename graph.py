from langgraph.graph import StateGraph, START, END
from state import JournalState
from nodes import analyze_mood, extract_tags, generate_reflection, log_history
from pathlib import Path

def build_graph():
    builder = StateGraph(JournalState)

    builder.add_node("Mood", analyze_mood)
    builder.add_node("Tags", extract_tags)
    builder.add_node("Reflection", generate_reflection)
    builder.add_node("Log History", log_history)

    builder.add_edge(START, "Mood")
    builder.add_edge("Mood","Tags")
    builder.add_edge("Tags", "Reflection")
    builder.add_edge("Reflection", "Log History")
    builder.add_edge("Log History", END)

    mood_journal_agent_graph = builder.compile()



    png_bytes = mood_journal_agent_graph.get_graph().draw_mermaid_png()

    output_path = Path("mood_journal_agent_graph_flow.png")
    output_path.write_bytes(png_bytes)

    print(f"Graph saved to {output_path.resolve()}")

    return mood_journal_agent_graph