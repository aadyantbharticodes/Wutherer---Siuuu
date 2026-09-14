from __future__ import annotations
import time
from collections import defaultdict
from typing import Optional, Hashable
import discord
from discord.ext import commands


class CooldownBucket:

    def __init__(self, rate: int, per: float):
        self.rate = rate
        self.per = per
        self._tokens: dict[Hashable, list[float]] = defaultdict(list)

    def get_retry_after(self, key: Hashable) -> Optional[float]:
        now = time.time()
        window = now - self.per
        tokens = [t for t in self._tokens[key] if t > window]
        self._tokens[key] = tokens

        if len(tokens) >= self.rate:
            return tokens[0] + self.per - now
        return None

    def update_rate_limit(self, key: Hashable) -> Optional[float]:
        retry_after = self.get_retry_after(key)
        if retry_after is not None:
            return retry_after
        self._tokens[key].append(time.time())
        return None

    def reset(self, key: Hashable) -> None:
        self._tokens.pop(key, None)

    def clear(self) -> None:
        self._tokens.clear()


def tiered_cooldown(default_rate: int = 1, default_per: float = 5.0, premium_rate: int = 3, premium_per: float = 3.0):
    bucket = CooldownBucket(default_rate, default_per)
    premium_bucket = CooldownBucket(premium_rate, premium_per)

    async def predicate(ctx: commands.Context) -> bool:
        if await ctx.bot.is_owner(ctx.author):
            return True

        is_premium = False
        if ctx.guild and isinstance(ctx.author, discord.Member):
            is_premium = ctx.author.premium_since is not None

        active_bucket = premium_bucket if is_premium else bucket
        retry_after = active_bucket.update_rate_limit(ctx.author.id)

        if retry_after is not None:
            raise commands.CommandOnCooldown(
                commands.Cooldown(active_bucket.rate, active_bucket.per),
                retry_after,
                commands.BucketType.user
            )
        return True

    return commands.check(predicate)

