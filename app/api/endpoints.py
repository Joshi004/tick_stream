from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.db.session import get_db
from app.models.tick_data import TickData
from app.schemas.tick_data import TickDataCreate, TickDataResponse
from app.services.kite_service import KiteTickerService

# Create a singleton instance of KiteTickerService
kite_service = KiteTickerService()

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


@router.post("/stream-ticks/subscribe/{instrument_code}")
async def subscribe_to_ticks(instrument_code: str, background_tasks: BackgroundTasks):
    """
    Subscribe to real-time ticks for a specific instrument
    
    This endpoint initiates a WebSocket connection to the Kite Connect API
    and subscribes to tick data for the specified instrument code.
    The ticks will be logged to the console.
    """
    try:
        # Start the ticker service if not already running
        if not kite_service.ticker or not kite_service.ticker.is_connected():
            background_tasks.add_task(kite_service.start)
            
        # Subscribe to the specified instrument
        success = kite_service.subscribe_instrument(instrument_code)
        
        if success:
            return {
                "status": "success",
                "message": f"Started streaming ticks for instrument {instrument_code}",
                "instrument_code": instrument_code
            }
        else:
            raise HTTPException(status_code=400, detail=f"Failed to subscribe to instrument {instrument_code}")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting tick stream: {str(e)}")
