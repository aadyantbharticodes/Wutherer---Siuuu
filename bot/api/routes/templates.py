from __future__ import annotations
from typing import Optional
from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

from database.models.templates import ServerTemplateModel
from services.templates import TemplateEngine, PUBLIC_TEMPLATES

router = APIRouter(prefix="/templates", tags=["Templates"])


class CreateTemplatePayload(BaseModel):
    name: str
    description: Optional[str] = ""
    is_public: Optional[bool] = False
    category: Optional[str] = "general"


class ApplyTemplatePayload(BaseModel):
    mode: Optional[str] = "merge"


@router.get("/public")
async def get_public_templates():
    return {
        "templates": [
            {
                "id": key,
                "name": val["name"],
                "description": val["description"],
                "category": val["category"],
                "roles_count": len(val.get("roles", [])),
                "categories_count": len(val.get("categories", []))
            }
            for key, val in PUBLIC_TEMPLATES.items()
        ]
    }


@router.get("/guild/{guild_id}")
async def get_guild_templates(guild_id: int, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    templates = await ServerTemplateModel.list_guild(bot.db, guild_id)
    return {"templates": templates}


@router.post("/guild/{guild_id}/create")
async def create_template(guild_id: int, payload: CreateTemplatePayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    guild = bot.get_guild(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    data = TemplateEngine.serialize_guild(guild)
    tid = await ServerTemplateModel.create(
        bot.db,
        guild_id=guild_id,
        creator_id=guild.owner_id or 0,
        name=payload.name,
        description=payload.description or "",
        data=data,
        is_public=payload.is_public or False,
        category=payload.category or "general"
    )
    return {"success": True, "template_id": tid}


@router.post("/guild/{guild_id}/apply/{template_id}")
async def apply_template(guild_id: int, template_id: str, payload: ApplyTemplatePayload, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    guild = bot.get_guild(guild_id)
    if not guild:
        raise HTTPException(status_code=404, detail="Guild not found")

    target_data = None
    if template_id in PUBLIC_TEMPLATES:
        target_data = PUBLIC_TEMPLATES[template_id]
    else:
        t = await ServerTemplateModel.get(bot.db, template_id)
        if t:
            target_data = t.get("data")

    if not target_data:
        raise HTTPException(status_code=404, detail="Template not found")

    mode = "wipe" if payload.mode == "wipe" else "merge"
    results = await TemplateEngine.apply_template(guild, target_data, mode=mode)
    return {"success": True, "results": results}


@router.delete("/{template_id}")
async def delete_template(template_id: str, request: Request):
    bot = getattr(request.app.state, "bot", None)
    if not bot:
        raise HTTPException(status_code=503, detail="Bot daemon unavailable")
    if template_id in PUBLIC_TEMPLATES:
        raise HTTPException(status_code=400, detail="Cannot delete public system template")
    await ServerTemplateModel.delete(bot.db, template_id)
    return {"success": True}
