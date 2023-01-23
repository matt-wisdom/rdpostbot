from typing import List, Optional
import pydantic


class Message(pydantic.BaseModel):
    title: str
    body: Optional[str]
    subreddits: List[str]
    interval: int
    flair: Optional[str]
    images: Optional[List[str]]
    comment: Optional[str]


class Messages(pydantic.BaseModel):
    messages: List[Message]
