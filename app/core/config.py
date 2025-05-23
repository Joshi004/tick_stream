import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PROJECT_NAME: str = "Tick Stream"
    
    # KITE CONNECT API
    KITE_API_KEY: Optional[str] = None
    KITE_ACCESS_TOKEN: Optional[str] = None
    
    # POSTGRES
    POSTGRES_SERVER: str = "timescaledb"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "tick_stream_db"
    POSTGRES_PORT: str = "5432"
    DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URI", mode="before")
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        # Convert port string to integer before passing to PostgresDsn.build
        port_str = values.data.get("POSTGRES_PORT")
        port = int(port_str) if port_str else 5432
        
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.data.get("POSTGRES_USER"),
            password=values.data.get("POSTGRES_PASSWORD"),
            host=values.data.get("POSTGRES_SERVER"),
            port=port,
            path=f"{values.data.get('POSTGRES_DB') or ''}",  # Removed leading slash
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
