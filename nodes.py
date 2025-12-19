from dotenv import load_dotenv
from langchain_groq import ChatGroq
import re
from typing import Dict, List
from state import JournalState

load_dotenv()

llm = ChatGroq(
    model="meta-llama/llama-4-maverick-17b-128e-instruct",
    temperature=0.0,
    max_retries=2,
)


def analyze_mood(state: JournalState) -> Dict[str, str]:
    """
    Reads:
        - state["entry_text"]

    Writes (returns update for):
        - "sentiment": Literal["positive", "negative", "neutral"]

    Responsibility:
        - Inspect entry_text via the LLM
        - Decide whether the overall emotional tone is positive, neutral, or negative
        - Return a partial state update dict like {"sentiment": "..."}
    """

    user_input = state["entry_text"]

    # Fallback: if entry is empty or only whitespace, default to neutral
    if not user_input or not user_input.strip():
        return {"sentiment": "neutral"}

    classification_prompt = f"""
You are a mood classifier for a personal journal app.
Your task is to read a short journal entry and classify the overall emotional tone.

You must respond with exactly one word, chosen from this list:
- positive
- neutral
- negative

Use these examples as a guide:

Example 1
Entry: "Had a great day, finished my tasks and enjoyed dinner with friends."
Label: positive

Example 2
Entry: "Today was okay. Nothing special happened, just went through the routine."
Label: neutral

Example 3
Entry: "Feeling exhausted and stressed. Too many meetings and I didn't finish my work."
Label: negative

Rules:
- If the entry feels mostly upbeat, grateful, satisfied, or happy -> respond positive.
- If the entry feels mostly stressed, sad, upset, frustrated, or overwhelmed -> respond negative.
- If the entry feels mixed, flat, factual, or unclear -> respond neutral.
- Do not explain your reasoning.
- Do not output anything else. Only one word: positive, neutral, or negative.
- Calm/relaxed can be positive; routine/ordinary with no emotion is neutral.

Journal entry:
<entry>
{user_input}
</entry>

Your answer (one word only):
"""

    # Call the LLM. For ChatGroq, .invoke(prompt) returns an AIMessage-like object.
    response = llm.invoke(classification_prompt)

    # Extract raw text from the response
    if hasattr(response, "content"):
        label_raw = response.content.strip().lower()
    else:
        # Fallback if the client returns a plain string or something else
        label_raw = str(response).strip().lower()

    # Normalize to one of the allowed labels
    allowed_labels = {"positive", "negative", "neutral"}
    label = label_raw

    # If the model returns extra text, try using the first word
    if label not in allowed_labels:
        words = label.split()
        if words:
            first_word = words[0].lower()
        else:
            first_word= ""

        if first_word in allowed_labels:
            label = first_word
        else:
            label = "neutral"

    return {"sentiment": label}



def extract_tags(state: JournalState) -> Dict[str, List[str]]:
    user_input = state["entry_text"]

    # ✅ Fix: correctly detect empty/whitespace-only input
    if not user_input or not user_input.strip():
        return {"tags": []}

    tags_prompt = f"""You are a tag generator for a personal mood journal app.
Your task is to read a short journal entry and extract 2 to 5 high-level themes.

Rules:
- Return only a comma-separated list of single-word, lowercase tags.
- Each tag should be a general theme (work, family, health, stress, energy, relationships, productivity, rest, motivation, burnout, focus).
- Do NOT include explanations.
- Do NOT repeat the same word.
- Do NOT include punctuation other than commas between tags.
- If you break the format, you fail. Output must be ONLY the tags line.
- Drop 1-letter tokens (like i)
- Drop common meta words (revised, wait, sorry, correction, etc.)
- Only include emotions like stress/burnout if explicitly stated.

Example output:
work, stress, meetings

Journal entry:
<entry>
{user_input}
</entry>

Your answer (comma-separated tags only):
"""

    response = llm.invoke(tags_prompt)

    # Extract raw text from the response
    if hasattr(response, "content"):
        raw = response.content
    else:
        raw = str(response)

    raw = raw.strip().lower()

    if not raw:
        return {"tags": []}

    # ✅ Fix: handle newlines / rambles by turning newlines into commas
    raw = raw.replace("\n", ",")

    seen = set()
    tags: List[str] = []

    for item in raw.split(","):
        item = item.strip()
        if not item:
            continue

        # ✅ Fix: if model rambles, keep only the first token
        item = item.split()[0]

        # ✅ Fix: remove weird punctuation, keep letters/numbers/hyphen
        item = re.sub(r"[^a-z0-9-]", "", item)

        if item and item not in seen:
            seen.add(item)
            tags.append(item)

        # ✅ Optional: stop once we have 5 tags
        if len(tags) == 4:
            break

    return {"tags": tags}






def generate_reflection(state: JournalState) -> dict:
    """
    Reads:
        - state["entry_text"]
        - state["sentiment"]
        - state["tags"]

    Writes (returns update for):
        - "reflection": str

    Responsibility:
        - Use sentiment + tags + original entry to generate 2–4 sentences:
            - emotionally validating
            - gently reflective
            - possibly suggesting 1 small action or perspective shift
        - Tone: supportive, non-judgmental, concise.
    """
    user_input = state["entry_text"]
    sentiment = state["sentiment"]
    tags = state["tags"]

    reflection_prompt = f"""You are a supportive reflection writer for a personal mood journal app.
    Your task is to write a short, thoughtful reflection based on a journal entry.
Rules:
- Write 2 to 4 sentences only.
- Match the tone to the given sentiment:
  - positive -> affirming and encouraging
  - neutral -> calm and reflective
  - negative -> supportive and validating
- Include at least ONE tag word exactly as written (copy the word into the reflection).
- Be gentle, empathetic, and human.
- Do NOT give direct advice.
- Do NOT ask questions.
- Do NOT use bullet points.
- Do NOT use therapy or coaching language.
- Do NOT say "you should".
- Avoid phrases like: "brave first step", "crucial step", "guide you", "find relief".
- Do NOT mention the rules or your reasoning.
- If you break the format, you fail. Output must be ONLY the reflection text.
- Avoid repeating the same tag more than once.
- Avoid phrases like ‘significant recognition’, ‘indicator’, ‘managing effectively’.
- Write exactly 2 to 4 sentences. Do not write 1 long sentence.

    Journal entry:
    <entry>
    {user_input}
    </entry>

    Sentiment:
    {sentiment}

    Tags:
    {tags}

    Your answer (reflection text only):
    """
    response = llm.invoke(reflection_prompt)

    if hasattr(response, "content"):
        text = response.content.strip()
    else:
        text = str(response).strip()


    return {"reflection": text}


def log_history(state: JournalState) -> dict:
    """
    Reads:
        - state["reflection"]
        - state["history"]

    Writes (returns update for):
        - "history": list[str]

    Responsibility:
        - Append the current reflection to the history list.
    """

    reflection = state["reflection"]
    history = state["history"]

    # If there's no reflection, don't change history
    if not reflection:
        return {"history": history}

    # First entry: history does not exist yet
    if history is None:
        new_history = [reflection]
    else:
        # Append to existing history
        new_history = history + [reflection]

    return {"history": new_history}

def gratitude_branch(state: "JournalState") -> dict:
    """
    Reads:
        - state["entry_text"]
        - state["sentiment"]

    Writes (returns update for):
        - Option 1: modifies "reflection" to include a gratitude angle
        - Option 2: adds a new field later like "gratitude_note" (not yet in state)
          (for now, you can just adjust "reflection")

    Responsibility:
        - If mood is negative, add a gentle reframe:
            - Ask the user to notice 1–2 things that were okay or good today.
            - Encourage a balanced view without invalidating their feelings.
        - Typically called BEFORE generate_reflection or as part of its logic,
          depending on how you wire the graph.
    """
    # TODO: Implement gratitude-style adjustment or prompt
    ...