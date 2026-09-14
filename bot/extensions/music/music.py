from __future__ import annotations
import asyncio
from typing import Optional

import discord
from discord.ext import commands

from core.cog import WuthererCog
from config import BOT_COLOR, BOT_COLOR_SUCCESS, BOT_COLOR_ERROR, BOT_COLOR_WARNING


class GuildMusicState:

    def __init__(self):
        self.queue: list[dict] = []
        self.current: Optional[dict] = None
        self.loop: bool = False
        self.volume: float = 1.0


class Music(WuthererCog):

    def __init__(self, bot):
        super().__init__(bot)
        self.states: dict[int, GuildMusicState] = {}

    def get_state(self, guild_id: int) -> GuildMusicState:
        if guild_id not in self.states:
            self.states[guild_id] = GuildMusicState()
        return self.states[guild_id]

    @commands.command(name="join", aliases=["connect"])
    async def join_channel(self, ctx: commands.Context, channel: Optional[discord.VoiceChannel] = None):
        target = channel or (ctx.author.voice.channel if ctx.author.voice else None)
        if not target:
            return await ctx.send("You are not connected to a voice channel.")

        vc = ctx.guild.voice_client
        if vc and vc.is_connected():
            await vc.move_to(target)
        else:
            await target.connect()
        await ctx.send(embed=discord.Embed(
            description=f"Connected to {target.mention}.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="leave", aliases=["disconnect", "dc"])
    async def leave_channel(self, ctx: commands.Context):
        vc = ctx.guild.voice_client
        if not vc or not vc.is_connected():
            return await ctx.send("I am not connected to a voice channel.")
        await vc.disconnect()
        self.states.pop(ctx.guild.id, None)
        await ctx.send(embed=discord.Embed(
            description="Disconnected from voice channel.",
            color=BOT_COLOR_SUCCESS
        ))

    @commands.command(name="play", aliases=["p"])
    async def play_audio(self, ctx: commands.Context, *, query: str):
        if not ctx.author.voice:
            return await ctx.send("You must be in a voice channel to play music.")

        vc = ctx.guild.voice_client
        if not vc:
            await ctx.author.voice.channel.connect()
            vc = ctx.guild.voice_client

        state = self.get_state(ctx.guild.id)
        song = {"title": query, "url": query, "requester": ctx.author}
        state.queue.append(song)

        if not vc.is_playing() and not vc.is_paused():
            state.current = state.queue.pop(0)
            embed = discord.Embed(
                title="🎵 Now Playing",
                description=f"**{state.current['title']}**\nRequested by {ctx.author.mention}",
                color=BOT_COLOR
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="📥 Added to Queue",
                description=f"**{song['title']}** (Position #{len(state.queue)})",
                color=BOT_COLOR_SUCCESS
            )
            await ctx.send(embed=embed)

    @commands.command(name="pause")
    async def pause_audio(self, ctx: commands.Context):
        vc = ctx.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await ctx.send("⏸️ Paused playback.")
        else:
            await ctx.send("Nothing is currently playing.")

    @commands.command(name="resume")
    async def resume_audio(self, ctx: commands.Context):
        vc = ctx.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await ctx.send("▶️ Resumed playback.")
        else:
            await ctx.send("Playback is not paused.")

    @commands.command(name="skip", aliases=["next"])
    async def skip_audio(self, ctx: commands.Context):
        vc = ctx.guild.voice_client
        state = self.get_state(ctx.guild.id)
        if not vc or not state.current:
            return await ctx.send("Nothing is currently playing.")

        if state.queue:
            state.current = state.queue.pop(0)
            await ctx.send(embed=discord.Embed(
                description=f"⏭️ Skipped to **{state.current['title']}**.",
                color=BOT_COLOR_SUCCESS
            ))
        else:
            state.current = None
            if vc.is_playing():
                vc.stop()
            await ctx.send("⏭️ Skipped track. Queue is now empty.")

    @commands.command(name="queue", aliases=["q"])
    async def view_queue(self, ctx: commands.Context):
        state = self.get_state(ctx.guild.id)
        embed = discord.Embed(title="🎶 Music Queue", color=BOT_COLOR)
        if state.current:
            embed.add_field(name="Currently Playing", value=f"**{state.current['title']}**", inline=False)

        if state.queue:
            lines = [f"`{i+1}.` {s['title']}" for i, s in enumerate(state.queue[:10])]
            embed.add_field(name="Up Next", value="\n".join(lines), inline=False)
            embed.set_footer(text=f"Total tracks in queue: {len(state.queue)}")
        else:
            embed.add_field(name="Up Next", value="No upcoming songs in queue.", inline=False)

        await ctx.send(embed=embed)

    @commands.command(name="nowplaying", aliases=["np"])
    async def now_playing(self, ctx: commands.Context):
        state = self.get_state(ctx.guild.id)
        if not state.current:
            return await ctx.send("Nothing is currently playing.")

        embed = discord.Embed(
            title="🎵 Now Playing",
            description=f"**{state.current['title']}**\nRequested by {state.current['requester'].mention}",
            color=BOT_COLOR
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))

