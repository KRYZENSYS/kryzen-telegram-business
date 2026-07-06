from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, ConfigDict
class BusinessOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; business_connection_id: str; business_name: str | None
    can_reply: bool; status: str; enabled: bool
    connected_at: datetime | None; disconnected_at: datetime | None; created_at: datetime
