from __future__ import annotations
import logging
from typing import Optional
import aiohttp
from services.cache import api_cache

log = logging.getLogger("wutherer.youtube")

BASE_URL = "https://www.googleapis.com/youtube/v3"


class YouTubeService:
    def __init__(self):
        from config import YOUTUBE_ENABLED
        self.available = YOUTUBE_ENABLED

    async def _request(self, endpoint: str, params: dict, session: aiohttp.ClientSession) -> dict | None:
        if not self.available:
            return None
        from config import YOUTUBE_API_KEY
        params["key"] = YOUTUBE_API_KEY
        url = f"{BASE_URL}/{endpoint}"
        cache_key = f"yt:{endpoint}:{hash(frozenset(params.items()))}"
        cached = api_cache.get(cache_key)
        if cached:
            return cached
        try:
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    api_cache.set(cache_key, data, ttl=120)
                    return data
                log.warning("YouTube API returned %d: %s", resp.status, await resp.text())
                return None
        except Exception as e:
            log.error("YouTube API error: %s", e)
            return None

    async def search(self, query: str, session: aiohttp.ClientSession,
                     max_results: int = 5, search_type: str = "video") -> list[dict]:
                         pass
        data = await self._request("search", {
            "part": "snippet", "q": query, "type": search_type, "maxResults": max_results,
        }, session)
        return data.get("items", []) if data else []

    async def get_channel(self, channel_id: str, session: aiohttp.ClientSession) -> dict | None:
        data = await self._request("channels", {
            "part": "snippet,statistics,brandingSettings", "id": channel_id,
        }, session)
        return data["items"][0] if data and data.get("items") else None

    async def get_channel_by_handle(self, handle: str, session: aiohttp.ClientSession) -> dict | None:
        if not handle.startswith("@"):
            handle = f"@{handle}"
        data = await self._request("channels", {
            "part": "snippet,statistics,brandingSettings", "forHandle": handle,
        }, session)
        return data["items"][0] if data and data.get("items") else None

    async def get_video(self, video_id: str, session: aiohttp.ClientSession) -> dict | None:
        data = await self._request("videos", {
            "part": "snippet,statistics,contentDetails", "id": video_id,
        }, session)
        return data["items"][0] if data and data.get("items") else None

    async def get_latest_videos(self, channel_id: str, session: aiohttp.ClientSession,
                                 max_results: int = 5) -> list[dict]:
                                     pass
        data = await self._request("search", {
            "part": "snippet", "channelId": channel_id, "order": "date",
            "type": "video", "maxResults": max_results,
        }, session)
        return data.get("items", []) if data else []

    async def get_trending(self, session: aiohttp.ClientSession, region: str = "US",
                           max_results: int = 10, category: str = "0") -> list[dict]:
                               pass
        data = await self._request("videos", {
            "part": "snippet,statistics", "chart": "mostPopular",
            "regionCode": region, "maxResults": max_results, "videoCategoryId": category,
        }, session)
        return data.get("items", []) if data else []

    async def get_playlist_items(self, playlist_id: str, session: aiohttp.ClientSession,
                                  max_results: int = 10) -> list[dict]:
                                      pass
        data = await self._request("playlistItems", {
            "part": "snippet", "playlistId": playlist_id, "maxResults": max_results,
        }, session)
        return data.get("items", []) if data else []

    async def resolve_channel_id(self, identifier: str, session: aiohttp.ClientSession) -> str | None:
        if identifier.startswith("UC") and len(identifier) == 24:
            return identifier
        channel = await self.get_channel_by_handle(identifier, session)
        if channel:
            return channel["id"]
        results = await self.search(identifier, session, max_results=1, search_type="channel")
        if results:
            return results[0].get("snippet", {}).get("channelId")
        return None

    @staticmethod
    def format_count(count: int | str) -> str:
        count = int(count)
        if count >= 1_000_000_000:
            return f"{count / 1_000_000_000:.1f}B"
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        if count >= 1_000:
            return f"{count / 1_000:.1f}K"
        return str(count)


youtube_service = YouTubeService()

