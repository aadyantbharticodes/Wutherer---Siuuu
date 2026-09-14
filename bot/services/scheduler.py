from __future__ import annotations
import asyncio
import datetime
import logging
from typing import Callable, Coroutine, Any, Dict

log = logging.getLogger("wutherer.scheduler")


class AsyncScheduler:

    def __init__(self):
        self._tasks: Dict[str, asyncio.Task] = {}

    def schedule(
        self,
        task_id: str,
        delay_seconds: float,
        coro_func: Callable[..., Coroutine[Any, Any, None]],
        *args,
        **kwargs
    ) -> None:
        self.cancel(task_id)

        async def _runner():
            try:
                await asyncio.sleep(delay_seconds)
                await coro_func(*args, **kwargs)
            except asyncio.CancelledError:
                pass
            except Exception as exc:
                log.error("Error in scheduled task '%s': %s", task_id, exc, exc_info=True)
            finally:
                self._tasks.pop(task_id, None)

        self._tasks[task_id] = asyncio.create_task(_runner())

    def cancel(self, task_id: str) -> bool:
        task = self._tasks.pop(task_id, None)
        if task and not task.done():
            task.cancel()
            return True
        return False

    def cancel_all(self) -> None:
        for task in self._tasks.values():
            if not task.done():
                task.cancel()
        self._tasks.clear()


scheduler = AsyncScheduler()

