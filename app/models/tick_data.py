from sqlalchemy import Column, Float, String, DateTime, Integer
from sqlalchemy.sql import func

from app.db.session import Base


class TickData(Base):
    __tablename__ = "tick_data"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    def __repr__(self):
        return f"<TickData(symbol='{self.symbol}', price={self.price}, volume={self.volume}, timestamp={self.timestamp})>" 