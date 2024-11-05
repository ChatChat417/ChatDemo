# api/models.py
from pydantic import BaseModel
from typing import List, Optional,Any,Dict

from pydantic import BaseModel
from typing import List, Optional

class Character(BaseModel):
    name: str
    background: str
    personality: str

class Scene(BaseModel):
    description: str
    mood: Optional[str] = None

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    character: Character
    scene: Scene
    message: str
    message_history: Optional[List[Message]] = []



