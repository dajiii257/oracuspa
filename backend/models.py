# Pydantic модели для API

from pydantic import BaseModel
from typing import Optional, List


class BatchCreateRequest(BaseModel):
    section: int
    count: int


class ClaimRequest(BaseModel):
    listing: str


class PrefsUpdateRequest(BaseModel):
    template: Optional[str] = None
    price_on: Optional[bool] = None
    price_mode: Optional[str] = None
    price_value: Optional[float] = None
    link: Optional[str] = None
    batch: Optional[int] = None
    haptics: Optional[bool] = None
    fullscreen: Optional[bool] = None
    notify: Optional[bool] = None
    custom: Optional[dict] = None
