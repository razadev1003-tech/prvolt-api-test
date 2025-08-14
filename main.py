from __future__ import annotations

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Query, status

from client import HunterIOClient
from config import settings
from schemas import DomainSearchResponse, EmailVerifyResponse

app = FastAPI(title="prvolt-api", version="0.1.0")


async def get_client() -> HunterIOClient:
    if not settings().api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="HUNTER_IO_API_KEY is not configured"
        )

    return HunterIOClient()


DomainParam = Annotated[str, Query(min_length=3)]
EmailParam = Annotated[str, Query()]
HttpClientParam = Annotated[HunterIOClient, Depends(get_client)]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/domains/search", response_model=DomainSearchResponse)
async def domains_search(
    domain: DomainParam,
    client: HttpClientParam,
) -> DomainSearchResponse:
    try:
        return await client.domain_search(domain)
    finally:
        await client.close()


@app.get("/emails/verify", response_model=EmailVerifyResponse)
async def emails_verify(
    email: EmailParam,
    client: HttpClientParam,
) -> EmailVerifyResponse:
    try:
        return await client.email_verify(email)
    finally:
        await client.close()
