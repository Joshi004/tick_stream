import time
from sqlalchemy.exc import OperationalError

from app.db.session import engine, Base
from app.models import TickData  # This ensures the models are imported
from app.db.init_db import init_db


def init():
    # Wait for database to be ready
    max_retries = 10
    retry_interval = 2  # seconds

    for i in range(max_retries):
        try:
            # Try to connect to the database
            from sqlalchemy import text
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            break
        except OperationalError:
            if i < max_retries - 1:
                print(f"Database not ready, retrying in {retry_interval} seconds... ({i+1}/{max_retries})")
                time.sleep(retry_interval)
            else:
                print("Max retries reached, database connection failed!")
                raise

    # Create tables
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")

    # Initialize TimescaleDB extensions and hypertables
    init_db()
    print("Database initialization completed!")


if __name__ == "__main__":
    init()
