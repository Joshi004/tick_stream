from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TickDataBase(BaseModel):
    symbol: str
    price: float
    volume: float


class TickDataCreate(TickDataBase):
    pass


class TickDataResponse(TickDataBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
        from_attributes = True 