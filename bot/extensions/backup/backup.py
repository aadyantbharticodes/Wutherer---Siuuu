from __future__ import annotations

import io
import json
import uuid
from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands

from bot.core.cog import WuthererCog
from bot.core.context import WuthererContext
from bot.core.checks import is_admin, is_server_owner
from bot.database.models.backup import BackupModel, GuildBackupSnapshot

if TYPE_CHECKING:
    from bot.core.bot import WuthererBot


class BackupConfirmView(discord.ui.View):

    def __init__(self, author_id: int) -> None:
        super().__init__(timeout=60.0)
        self.author_id = author_id
        self.confirmed: Optional[bool] = None

    @discord.ui.button(label="Confirm Restore", style=discord.ButtonStyle.danger, emoji="⚠️")
    async def confirm_btn(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command author can confirm this restore.", ephemeral=True)
            return
        self.confirmed = True
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary, emoji="✖️")
    async def cancel_btn(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command author can cancel this action.", ephemeral=True)
            return
        self.confirmed = False
        self.stop()
        await interaction.response.defer()


class Backup(WuthererCog, name="Backup"):

    def __init__(self, bot: WuthererBot) -> None:
        super().__init__(bot)

    @commands.group(name="backup", aliases=["snapshots", "bkp"], invoke_without_command=True)
    @is_admin()
    async def backup_group(self, ctx: WuthererContext) -> None:
        await ctx.send_help(ctx.command)

    @backup_group.command(name="create", aliases=["new", "save"])
    @is_admin()
    @commands.cooldown(1, 120, commands.BucketType.guild)
    async def backup_create(self, ctx: WuthererContext, *, notes: Optional[str] = None) -> None:
        guild = ctx.guild
        if not guild:
            return

        status_msg = await ctx.send_info("Capturing guild snapshot (roles, channels, permissions)...")


        roles_data = []
        for role in sorted(guild.roles, key=lambda r: r.position):
            if role.is_default():
                continue
            roles_data.append({
                "id": role.id,
                "name": role.name,
                "color": role.color.value,
                "hoist": role.hoist,
                "mentionable": role.mentionable,
                "permissions": role.permissions.value,
                "position": role.position,
            })


        categories_data = []
        for cat in guild.categories:
            categories_data.append({
                "id": cat.id,
                "name": cat.name,
                "position": cat.position,
            })

        channels_data = []
        for ch in guild.channels:
            if isinstance(ch, discord.CategoryChannel):
                continue
            channels_data.append({
                "id": ch.id,
                "name": ch.name,
                "type": str(ch.type),
                "category_id": ch.category_id,
                "position": ch.position,
                "topic": getattr(ch, "topic", None),
                "nsfw": getattr(ch, "nsfw", False),
            })


        emojis_data = [{"name": e.name, "url": str(e.url)} for e in guild.emojis[:50]]


        backup_id = f"snp_{uuid.uuid4().hex[:10]}"

        snapshot = GuildBackupSnapshot(
            backup_id=backup_id,
            guild_id=guild.id,
            guild_name=guild.name,
            created_by=ctx.author.id,
            roles_data=roles_data,
            categories_data=categories_data,
            channels_data=channels_data,
            emojis_data=emojis_data,
            notes=notes,
        )

        async with self.bot.db_pool.acquire() as db:
            dao = BackupModel(db)
            await dao.create_backup(snapshot)

        embed = self.bot.embed.create(
            title="🛡️ Server Backup Created",
            description=f"Snapshot successfully compiled and archived.\n**ID:** `{backup_id}`",
            color=self.bot.embed.COLOR_SUCCESS,
        )
        embed.add_field(name="Roles Saved", value=f"`{len(roles_data)}`", inline=True)
        embed.add_field(name="Channels Saved", value=f"`{len(channels_data)}`", inline=True)
        embed.add_field(name="Categories", value=f"`{len(categories_data)}`", inline=True)
        if notes:
            embed.add_field(name="Notes", value=notes, inline=False)
        embed.set_footer(text=f"Use s!backup restore {backup_id} to apply")

        await status_msg.edit(content=None, embed=embed)

    @backup_group.command(name="list")
    @is_admin()
    async def backup_list(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = BackupModel(db)
            backups = await dao.list_guild_backups(ctx.guild.id, limit=10)

        if not backups:
            await ctx.send_warn("No saved backups found for this server. Use `s!backup create` to make one.")
            return

        embed = self.bot.embed.create(
            title=f"📦 Server Backups — {ctx.guild.name}",
            description=f"Showing `{len(backups)}` most recent snapshots stored in Sentinel.",
        )

        for b in backups:
            created_ts = f"<t:{b.created_at}:R>"
            summary = f"• **Roles:** `{len(b.roles_data)}` | **Channels:** `{len(b.channels_data)}`\n• **Created:** {created_ts} by <@{b.created_by}>\n"
            if b.notes:
                summary += f"• *Notes:* {b.notes}"
            embed.add_field(name=f"Backup `{b.backup_id}`", value=summary, inline=False)

        await ctx.send(embed=embed)

    @backup_group.command(name="info", aliases=["view"])
    @is_admin()
    async def backup_info(self, ctx: WuthererContext, backup_id: str) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = BackupModel(db)
            backup = await dao.get_backup(backup_id)

        if not backup or backup.guild_id != ctx.guild.id:
            await ctx.send_error(f"Backup `{backup_id}` was not found in this guild's archives.")
            return

        embed = self.bot.embed.create(
            title=f"📄 Backup Metadata — {backup.backup_id}",
            description=f"Snapshot of **{backup.guild_name}** recorded on <t:{backup.created_at}:F>",
        )
        embed.add_field(name="Saved Roles", value=f"`{len(backup.roles_data)}` roles", inline=True)
        embed.add_field(name="Categories", value=f"`{len(backup.categories_data)}` categories", inline=True)
        embed.add_field(name="Channels", value=f"`{len(backup.channels_data)}` channels", inline=True)
        embed.add_field(name="Archived By", value=f"<@{backup.created_by}>", inline=True)
        if backup.notes:
            embed.add_field(name="Notes", value=backup.notes, inline=False)

        await ctx.send(embed=embed)

    @backup_group.command(name="download", aliases=["export"])
    @is_admin()
    async def backup_download(self, ctx: WuthererContext, backup_id: str) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = BackupModel(db)
            backup = await dao.get_backup(backup_id)

        if not backup or backup.guild_id != ctx.guild.id:
            await ctx.send_error(f"Backup `{backup_id}` not found.")
            return

        json_bytes = backup.to_json().encode("utf-8")
        file = discord.File(io.BytesIO(json_bytes), filename=f"{backup.backup_id}_{ctx.guild.id}.json")
        await ctx.send(f"📥 Export for backup `{backup_id}`:", file=file)

    @backup_group.command(name="restore", aliases=["apply"])
    @is_server_owner()
    @commands.cooldown(1, 300, commands.BucketType.guild)
    async def backup_restore(self, ctx: WuthererContext, backup_id: str) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = BackupModel(db)
            backup = await dao.get_backup(backup_id)

        if not backup or backup.guild_id != ctx.guild.id:
            await ctx.send_error(f"Backup `{backup_id}` not found.")
            return

        view = BackupConfirmView(ctx.author.id)
        prompt_embed = self.bot.embed.create(
            title="⚠️ Destructive Operation: Server Restore",
            description=(
                f"You are about to restore server topology from backup **`{backup_id}`**.\n\n"
                "**Restoration Actions:**\n"
                f"• Recreate missing roles (`{len(backup.roles_data)}` stored)\n"
                f"• Recreate missing channels & categories (`{len(backup.channels_data)}` channels)\n\n"
                "Are you absolutely certain you want to proceed?"
            ),
            color=self.bot.embed.COLOR_WARN,
        )
        msg = await ctx.send(embed=prompt_embed, view=view)
        await view.wait()

        if not view.confirmed:
            await msg.edit(content="❌ Server restoration cancelled.", embed=None, view=None)
            return

        progress_msg = await ctx.send_info("🔄 Restoring server structure... This may take up to a minute.")

        guild = ctx.guild
        restored_roles = 0
        restored_channels = 0


        existing_role_names = {r.name.lower() for r in guild.roles}
        for r_info in backup.roles_data:
            if r_info["name"].lower() not in existing_role_names:
                try:
                    await guild.create_role(
                        name=r_info["name"],
                        color=discord.Color(r_info.get("color", 0)),
                        hoist=r_info.get("hoist", False),
                        mentionable=r_info.get("mentionable", False),
                        reason=f"Sentinel Backup Restore: {backup_id}",
                    )
                    restored_roles += 1
                except discord.HTTPException:
                    pass


        existing_ch_names = {c.name.lower() for c in guild.channels}
        for ch_info in backup.channels_data:
            if ch_info["name"].lower() not in existing_ch_names:
                try:
                    if "voice" in ch_info.get("type", "").lower():
                        await guild.create_voice_channel(name=ch_info["name"], reason=f"Backup Restore: {backup_id}")
                    else:
                        await guild.create_text_channel(name=ch_info["name"], topic=ch_info.get("topic"), reason=f"Backup Restore: {backup_id}")
                    restored_channels += 1
                except discord.HTTPException:
                    pass

        success_embed = self.bot.embed.create(
            title="✅ Server Restoration Finished",
            description=f"Successfully restored missing components from backup `{backup_id}`.",
            color=self.bot.embed.COLOR_SUCCESS,
        )
        success_embed.add_field(name="Roles Created", value=f"`{restored_roles}`", inline=True)
        success_embed.add_field(name="Channels Created", value=f"`{restored_channels}`", inline=True)

        await progress_msg.edit(content=None, embed=success_embed)

    @backup_group.command(name="delete", aliases=["remove"])
    @is_admin()
    async def backup_delete(self, ctx: WuthererContext, backup_id: str) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = BackupModel(db)
            deleted = await dao.delete_backup(backup_id, ctx.guild.id)

        if deleted:
            await ctx.send_success(f"Snapshot `{backup_id}` has been deleted.")
        else:
            await ctx.send_error(f"Could not find or delete snapshot `{backup_id}`.")


async def setup(bot: WuthererBot) -> None:
    await bot.add_cog(Backup(bot))

