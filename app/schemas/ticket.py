from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TicketBase(BaseModel):
    title: str
    description: str
    tags: list[str] = Field(default_factory=list)


class TicketCreate(TicketBase):
    author_id: int


class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    tags: list[str] | None = None


class TicketRead(TicketBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    author_id: int
    created_at: datetime
