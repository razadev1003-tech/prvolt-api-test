from __future__ import annotations

from typing import Any, Dict, Optional, Type, TypeVar

import httpx
from fastapi import status
from pydantic import BaseModel, AnyHttpUrl

from config import settings
from schemas import DomainSearchResponse, EmailVerifyResponse

TModel = TypeVar("TModel", bound=BaseModel)


class HttpClientConfig(BaseModel):
    base_url: AnyHttpUrl
    timeout_seconds: float
    max_retries: int


class HunterIOClient:
    def __init__(self) -> None:
        cfg = settings()
        self._cfg = HttpClientConfig(
            base_url=cfg.api_url,  # type: ignore[arg-type]  # pydantic coerces str -> AnyHttpUrl
            timeout_seconds=cfg.timeout_seconds,
            max_retries=cfg.max_retries,
        )
        self._api_key = cfg.api_key
        self._client = httpx.AsyncClient(
            base_url=str(self._cfg.base_url),
            timeout=self._cfg.timeout_seconds,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def domain_search(self, domain: str) -> DomainSearchResponse:
        return await self._get_model(
            path="/domain-search",
            query_params={"domain": domain},
            model=DomainSearchResponse,
        )

    async def email_verify(self, email: str) -> EmailVerifyResponse:
        return await self._get_model(
            path="/email-verifier",
            query_params={"email": email},
            model=EmailVerifyResponse,
        )

    async def _get_model(
        self,
        *,
        path: str,
        query_params: Dict[str, Any],
        model: Type[TModel],
    ) -> TModel:
        """
        Make a GET request and validate the response body directly into a Pydantic model.
        """
        attempts = 0
        last_error: Optional[Exception] = None
        full_query = {**query_params, "api_key": self._api_key}

        while attempts <= self._cfg.max_retries:
            attempts += 1
            try:
                response = await self._client.get(path, params=full_query)
            except Exception as exc:  # noqa: WPS429
                last_error = exc
                continue

            if status.HTTP_200_OK <= response.status_code < status.HTTP_300_MULTIPLE_CHOICES:
                return model.model_validate_json(response.text)

            last_error = RuntimeError(
                f"HTTP {response.status_code} for {path} with {full_query!r}",
            )

        assert last_error is not None
        raise last_error
