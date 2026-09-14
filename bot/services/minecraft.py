from __future__ import annotations
import logging
from typing import Optional
import aiohttp
from services.cache import api_cache

log = logging.getLogger("wutherer.minecraft")

MOJANG_API = "https://api.mojang.com"
SESSIONSERVER = "https://sessionserver.mojang.com"
CRAFATAR = "https://crafatar.com"


class MinecraftService:
    async def get_uuid(self, username: str, session: aiohttp.ClientSession) -> Optional[str]:
        cache_key = f"mc:uuid:{username.lower()}"
        cached = api_cache.get(cache_key)
        if cached:
            return cached
        try:
            async with session.get(f"{MOJANG_API}/users/profiles/minecraft/{username}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    uuid = data.get("id")
                    if uuid:
                        api_cache.set(cache_key, uuid, ttl=3600)
                    return uuid
                return None
        except Exception as e:
            log.error("Mojang UUID lookup error: %s", e)
            return None

    async def get_profile(self, uuid: str, session: aiohttp.ClientSession) -> Optional[dict]:
        cache_key = f"mc:profile:{uuid}"
        cached = api_cache.get(cache_key)
        if cached:
            return cached
        try:
            async with session.get(f"{SESSIONSERVER}/session/minecraft/profile/{uuid}") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    api_cache.set(cache_key, data, ttl=600)
                    return data
                return None
        except Exception as e:
            log.error("Mojang profile lookup error: %s", e)
            return None

    async def get_username_from_uuid(self, uuid: str, session: aiohttp.ClientSession) -> Optional[str]:
        profile = await self.get_profile(uuid, session)
        return profile.get("name") if profile else None

    def get_avatar_url(self, uuid: str, size: int = 128) -> str:
        return f"{CRAFATAR}/avatars/{uuid}?size={size}&overlay=true"

    def get_head_url(self, uuid: str, size: int = 128) -> str:
        return f"{CRAFATAR}/renders/head/{uuid}?size={size}&overlay=true"

    def get_body_url(self, uuid: str, size: int = 128) -> str:
        return f"{CRAFATAR}/renders/body/{uuid}?size={size}&overlay=true"

    def get_skin_url(self, uuid: str) -> str:
        return f"{CRAFATAR}/skins/{uuid}"

    async def query_server(self, address: str, port: int = None,
                           server_type: str = "java") -> Optional[dict]:
                               pass
        try:
            from mcstatus import JavaServer, BedrockServer
            if server_type == "bedrock":
                server = BedrockServer.lookup(f"{address}:{port or 19132}")
                status = await server.async_status()
                return {
                    "online": True,
                    "players_online": status.players_online,
                    "players_max": status.players_max,
                    "motd": str(status.motd),
                    "version": status.version.name,
                    "latency": round(status.latency, 1),
                    "gamemode": status.gamemode,
                    "map_name": status.map_name,
                    "type": "bedrock",
                }
            server = JavaServer.lookup(f"{address}:{port or 25565}")
            status = await server.async_status()
            player_list = []
            if status.players.sample:
                player_list = [p.name for p in status.players.sample]
            return {
                "online": True,
                "players_online": status.players.online,
                "players_max": status.players.max,
                "motd": str(status.description),
                "version": status.version.name,
                "latency": round(status.latency, 1),
                "favicon": status.favicon,
                "player_list": player_list,
                "type": "java",
            }
        except Exception as e:
            log.warning("MC server query failed for %s: %s", address, e)
            return {"online": False, "error": str(e)}

    async def get_hypixel_stats(self, uuid: str, api_key: str,
                                 session: aiohttp.ClientSession) -> Optional[dict]:
                                     pass
        if not api_key:
            return None
        try:
            async with session.get(
                "https://api.hypixel.net/player",
                params={"uuid": uuid, "key": api_key},
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("success"):
                        return data.get("player")
                return None
        except Exception as e:
            log.error("Hypixel API error: %s", e)
            return None


minecraft_service = MinecraftService()

