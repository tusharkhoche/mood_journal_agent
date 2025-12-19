from typing import Literal, TypedDict

class JournalState(TypedDict):

    entry_text: str
    sentiment: Literal["positive", "negative", "neutral"] | None
    tags: list[str] | None
    reflection: str | None
    history: list[str] | None



