from __future__ import annotations

from dotenv import load_dotenv
from pydantic import BaseModel, Field, AnyHttpUrl
import os

load_dotenv()

class HttpClientSettings(BaseModel):
    api_url: AnyHttpUrl = AnyHttpUrl("https://api.hunter.io/v2/")
    api_key: str = Field(default_factory=lambda: os.getenv("HUNTER_IO_API_KEY", ""))
    timeout_seconds: float = 10.0
    max_retries: int = 2


def settings() -> HttpClientSettings:
    return HttpClientSettings()
