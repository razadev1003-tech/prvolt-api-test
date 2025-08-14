from __future__ import annotations

from typing import Optional, List

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class DomainSearchData(BaseModel):
    domain: str
    disposable: Optional[bool] = None
    webmail: Optional[bool] = None
    accept_all: Optional[bool] = None
    pattern: Optional[str] = None
    organization: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    twitter: Optional[str] = None
    facebook: Optional[str] = None
    linkedin: Optional[str] = None
    instagram: Optional[str] = None
    youtube: Optional[str] = None
    technologies: List[str] = []
    country: Optional[str] = None
    state: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[str] = None
    street: Optional[str] = None
    headcount: Optional[str] = None
    company_type: Optional[str] = None
    linked_domains: List[str] = []


class DomainSearchResponse(BaseModel):
    payload: DomainSearchData = Field(alias="data")

    model_config = ConfigDict(populate_by_name=True)


class EmailVerifyData(BaseModel):
    email: EmailStr
    score: Optional[int] = Field(default=None, ge=0, le=100)
    regexp: Optional[bool] = None
    gibberish: Optional[bool] = None
    disposable: Optional[bool] = None
    webmail: Optional[bool] = None
    mx_records: Optional[bool] = None
    smtp_server: Optional[bool] = None
    smtp_check: Optional[bool] = None
    accept_all: Optional[bool] = None
    block: Optional[bool] = None


class EmailVerifyResponse(BaseModel):
    payload: EmailVerifyData = Field(alias="data")

    model_config = ConfigDict(populate_by_name=True)
