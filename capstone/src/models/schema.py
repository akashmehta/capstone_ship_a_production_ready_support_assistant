from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class Message(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class UserSessionState(BaseModel):
    session_id: str
    user_id: str
    history: List[Message] = Field(default_factory=list)

class OrderLookupInput(BaseModel):
    order_id: str = Field(..., pattern=r"^ORD-[A-Z0-9]{6}$", description="Standardized Order ID")

class APIResponseEnvelope(BaseModel):
    status: Literal["success", "error"]
    session_id: str
    data: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    tool_calls_executed: int = 0