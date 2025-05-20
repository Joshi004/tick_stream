from sqlalchemy.sql import text
from sqlalchemy.exc import ProgrammingError

from app.db.session import engine


def init_db():
    """Initialize database with TimescaleDB extension"""
    with engine.connect() as conn:
        # Create TimescaleDB extension if it doesn't exist
        try:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;"))
            conn.commit()
            print("TimescaleDB extension created or already exists")
        except ProgrammingError:
            print("Failed to create TimescaleDB extension - this is expected if not using TimescaleDB")
            conn.rollback()
            
        # Create hypertable for tick data
        try:
            conn.execute(text("""
                SELECT create_hypertable('tick_data', 'timestamp', if_not_exists => TRUE);
            """))
            conn.commit()
            print("Hypertable created or already exists")
        except ProgrammingError as e:
            print(f"Failed to create hypertable: {e}")
            conn.rollback() 