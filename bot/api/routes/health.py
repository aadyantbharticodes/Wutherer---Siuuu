from __future__ import annotations
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("")
async def healthcheck():
    return {"status": "healthy", "service": "sentinel-api"}

