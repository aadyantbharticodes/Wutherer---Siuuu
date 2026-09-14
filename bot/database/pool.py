import asyncio
import logging
import random
from pathlib import Path
from typing import Any, Optional

import aiosqlite

from config import DB_PATH

log = logging.getLogger("wutherer.db")


class DatabasePool:
    def __init__(self, path: Path = DB_PATH):
        self.path = path
        self._conn: Optional[aiosqlite.Connection] = None
        self._lock = asyncio.Lock()

    async def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = await aiosqlite.connect(str(self.path), timeout=30)
        self._conn.row_factory = aiosqlite.Row
        await self._conn.execute("PRAGMA journal_mode=WAL")
        await self._conn.execute("PRAGMA foreign_keys=ON")
        await self._conn.execute("PRAGMA busy_timeout=5000")
        await self._conn.commit()

        from .migrations import run_migrations
        await run_migrations(self)
        log.info("Database initialized at %s", self.path)

    async def close(self):
        if self._conn:
            await self._conn.close()
            self._conn = None

    async def execute(self, sql: str, params: tuple = ()) -> aiosqlite.Cursor:
        return await self._retry(lambda: self._conn.execute(sql, params))

    async def executemany(self, sql: str, params_seq) -> aiosqlite.Cursor:
        return await self._retry(lambda: self._conn.executemany(sql, params_seq))

    async def fetchone(self, sql: str, params: tuple = ()) -> Optional[dict]:
        cursor = await self.execute(sql, params)
        row = await cursor.fetchone()
        return dict(row) if row else None

    async def fetchall(self, sql: str, params: tuple = ()) -> list[dict]:
        cursor = await self.execute(sql, params)
        rows = await cursor.fetchall()
        return [dict(r) for r in rows]

    async def fetchval(self, sql: str, params: tuple = (), default: Any = None) -> Any:
        row = await self.fetchone(sql, params)
        if row:
            return list(row.values())[0]
        return default

    async def commit(self):
        if self._conn:
            await self._conn.commit()

    async def _retry(self, fn, retries: int = 5):
        for attempt in range(retries):
            try:
                return await fn()
            except aiosqlite.OperationalError as e:
                if "database is locked" in str(e).lower() and attempt < retries - 1:
                    wait = (2 ** attempt) + random.uniform(0, 1)
                    log.warning("Database locked, retrying in %.1fs...", wait)
                    await asyncio.sleep(wait)
                else:
                    raise
        raise RuntimeError("Database operation failed after retries")

