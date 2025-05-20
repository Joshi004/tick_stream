from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.tick_data import TickData
from app.schemas.tick_data import TickDataCreate, TickDataResponse

router = APIRouter()


@router.post("/tick", response_model=TickDataResponse)
def create_tick_data(tick: TickDataCreate, db: Session = Depends(get_db)):
    db_tick = TickData(**tick.model_dump())
    db.add(db_tick)
    db.commit()
    db.refresh(db_tick)
    return db_tick


@router.get("/tick/{symbol}", response_model=List[TickDataResponse])
def read_tick_data(symbol: str, db: Session = Depends(get_db)):
    ticks = db.query(TickData).filter(TickData.symbol == symbol).all()
    return ticks 