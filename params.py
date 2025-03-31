from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str


class NaiveChatRequest(BaseModel):
    context: list[str]
    messages: list[Message]