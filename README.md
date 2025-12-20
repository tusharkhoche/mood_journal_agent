# 🧠 Mood Journal Agent (LangGraph)

A beginner-friendly **LangGraph-based journaling agent** that analyzes daily journal entries, extracts emotional insights, generates reflective responses, and persists reflection history across runs.

This project was built as hands-on practice after completing the **LangGraph Essentials** course from LangChain Academy.

---

## ✨ Features

- 📝 Accepts a free-text daily journal entry
- 😊 Classifies overall **sentiment** (positive / neutral / negative)
- 🏷️ Extracts meaningful **tags** (themes like work, family, stress, rest)
- 💬 Generates a short, supportive **reflection**
- 📚 Maintains a persistent **history** of reflections using a JSON file
- 🔁 Fully orchestrated using **LangGraph StateGraph**

---

## 🧱 Architecture Overview

The agent is implemented as a **linear LangGraph pipeline**:

<img width="127" height="531" alt="mood_journal_agent_graph_flow" src="https://github.com/user-attachments/assets/45473f3a-6405-4802-8908-47b62824179a" />


Each node:
- Reads from shared state (`JournalState`)
- Returns a **partial state update**
- Is tested independently before being wired into the graph

---




## 🗂️ Project Structure

```text
.
├── state.py        # TypedDict defining the shared graph state
├── nodes.py        # LangGraph node implementations
├── graph.py        # StateGraph wiring
├── storage.py      # JSON-based history persistence
├── run.py          # CLI entry point
├── history.json    # Persisted reflection history (auto-created)
└── README.md

---
```

## 🧠 State Design

```python
class JournalState(TypedDict):
    entry_text: str
    sentiment: Literal["positive", "negative", "neutral"] | None
    tags: list[str] | None
    reflection: str | None
    history: list[str] | None

    
---
```
The entire agent operates by reading and updating this shared state.




## 🚀 How to Run
1️⃣ Install dependencies
'''python
pip install langgraph langchain-groq python-dotenv

---

Make sure you have a valid Groq API key set in your environment variables.

2️⃣ Run the agent
python run.py

---

You’ll be prompted:
How was your day?


Example input:
My day was fantastic. Enjoyed vacation time with family.

---
## 3️⃣ Example Output
Sentiment: positive
Tags: ['family', 'rest']
Reflection: Spending quality time with family can be truly uplifting...
History count: 3

---
Reflections are automatically saved to history.json.

## 💾 History Persistence
    Reflection history is stored in a local history.json file
    Loaded at startup
    Appended after each run
    Safely handles:
    Missing file
    Empty file
    Invalid JSON

This keeps the project simple while demonstrating real-world persistence.

---
## 🧪 Testing Approach
    Each node was tested independently before graph wiring:
    analyze_mood → sentiment classification
    extract_tags → robust tag parsing
    generate_reflection → tone & format validation
    log_history → append-only behavior
This mirrors best practices for LangGraph development.

---
## 🎯 Learning Goals Achieved

This project demonstrates:
    Core LangGraph concepts:
        StateGraph
        Shared state updates
        Node isolation
Prompt discipline vs post-processing
File-based persistence
CLI-based agent execution
Debugging and hardening LLM outputs

---
## 🔮 Possible Extensions
    Conditional branching using Command
    Human-in-the-loop pauses using Interrupt
    Weekly or monthly summary node
    SQLite-based persistence
    Web UI (FastAPI / Streamlit)
    Multi-entry sentiment trends

---
## 📜 License
    MIT License (or update as needed)

---
## 🙌 Acknowledgements
    LangChain Academy
    LangGraph documentation and examples
    Groq + LLaMA models

---
