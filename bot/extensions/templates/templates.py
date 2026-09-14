from __future__ import annotations
import json
import discord
from discord.ext import commands
from typing import Optional

from database.models.templates import ServerTemplateModel
from services.templates import TemplateEngine, PUBLIC_TEMPLATES


class ConfirmApplyView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=60.0)
        self.author_id = author_id
        self.confirmed = False

    @discord.ui.button(label="Confirm & Apply", style=discord.ButtonStyle.danger, emoji="⚠️")
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command author can confirm!", ephemeral=True)
            return
        self.confirmed = True
        self.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("Only the command author can cancel!", ephemeral=True)
            return
        self.confirmed = False
        self.stop()
        await interaction.response.send_message("Template application cancelled.", ephemeral=True)


class TemplatesCog(commands.Cog, name="Templates"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="template", aliases=["templates"], invoke_without_command=True)
    async def template_group(self, ctx: commands.Context):
        embed = discord.Embed(
            title="📋 Xenon Server Template Engine",
            description="Serialize, backup, share, and apply complete server channel, category, and role layouts.",
            color=0x5865F2
        )
        embed.add_field(name="Commands", value=(
            "`s!template create <name> [desc]` — Save current server layout as a template\n"
            "`s!template list` — List all templates created for this server\n"
            "`s!template public` — Browse curated public community templates\n"
            "`s!template preview <id>` — Preview channels and roles in a template\n"
            "`s!template apply <id> [--wipe]` — Apply a template to this server\n"
            "`s!template export <id>` — Export template JSON data\n"
            "`s!template delete <id>` — Delete a saved template"
        ), inline=False)
        embed.set_footer(text="Sentinel Template Core • Similar to Xenon bot")
        await ctx.send(embed=embed)

    @template_group.command(name="create")
    @commands.has_permissions(administrator=True)
    async def template_create(self, ctx: commands.Context, name: str, *, description: str = ""):
        msg = await ctx.send("⏳ Serializing guild layout, categories, channels, and role hierarchy...")
        data = TemplateEngine.serialize_guild(ctx.guild)
        tid = await ServerTemplateModel.create(
            self.bot.db,
            guild_id=ctx.guild.id,
            creator_id=ctx.author.id,
            name=name,
            description=description,
            data=data
        )

        role_count = len(data.get("roles", []))
        cat_count = len(data.get("categories", []))
        total_ch = sum(len(c.get("channels", [])) for c in data.get("categories", []))

        embed = discord.Embed(
            title="✅ Template Created Successfully",
            description=f"Server template **{name}** has been saved with ID: `{tid}`",
            color=0x57F287
        )
        embed.add_field(name="Template ID", value=f"`{tid}`", inline=True)
        embed.add_field(name="Categories", value=f"**{cat_count}**", inline=True)
        embed.add_field(name="Channels", value=f"**{total_ch}**", inline=True)
        embed.add_field(name="Roles Saved", value=f"**{role_count}**", inline=True)
        embed.set_footer(text=f"Apply anytime with: s!template apply {tid}")
        await msg.edit(content=None, embed=embed)

    @template_group.command(name="list")
    @commands.has_permissions(manage_guild=True)
    async def template_list(self, ctx: commands.Context):
        templates = await ServerTemplateModel.list_guild(self.bot.db, ctx.guild.id)
        if not templates:
            await ctx.send("ℹ️ No custom templates found for this server. Create one with `s!template create <name>`.")
            return

        embed = discord.Embed(
            title=f"📋 Saved Templates for {ctx.guild.name}",
            color=0x5865F2
        )
        for t in templates[:10]:
            data = t.get("data", {})
            cats = len(data.get("categories", []))
            roles = len(data.get("roles", []))
            embed.add_field(
                name=f"🔹 {t['name']} (`{t['id']}`)",
                value=f"{t.get('description') or '*No description*'}\n`{cats} categories` • `{roles} roles` • Created: `{t.get('created_at', '')[:10]}`",
                inline=False
            )
        await ctx.send(embed=embed)

    @template_group.command(name="public")
    async def template_public(self, ctx: commands.Context):
        embed = discord.Embed(
            title="🌐 Public Curated Community Templates",
            description="Production-grade Xenon-style server templates available to apply instantly.",
            color=0x9B59B6
        )
        for key, tmpl in PUBLIC_TEMPLATES.items():
            cats = len(tmpl.get("categories", []))
            roles = len(tmpl.get("roles", []))
            embed.add_field(
                name=f"⭐ {tmpl['name']} (`{key}`)",
                value=f"{tmpl['description']}\n`{cats} categories` • `{roles} roles` • Category: **{tmpl['category'].title()}**\nApply with: `s!template apply {key}`",
                inline=False
            )
        await ctx.send(embed=embed)

    @template_group.command(name="preview")
    async def template_preview(self, ctx: commands.Context, template_id: str):
        target_data = None
        name = template_id

        if template_id in PUBLIC_TEMPLATES:
            target_data = PUBLIC_TEMPLATES[template_id]
            name = target_data["name"]
        else:
            t = await ServerTemplateModel.get(self.bot.db, template_id)
            if t:
                target_data = t.get("data")
                name = t["name"]

        if not target_data:
            await ctx.send("❌ Template not found! Check `s!template list` or `s!template public`.")
            return

        embed = discord.Embed(
            title=f"🔍 Template Preview: {name}",
            description=target_data.get("description", "*No description*"),
            color=0x5865F2
        )

        roles = [r["name"] for r in target_data.get("roles", [])]
        embed.add_field(name=f"Roles ({len(roles)})", value=", ".join(roles[:12]) + ("..." if len(roles) > 12 else "") or "*None*", inline=False)

        cats_desc = []
        for cat in target_data.get("categories", []):
            ch_names = [f"#{ch['name']}" if ch.get("type") == "text" else f"🔊 {ch['name']}" for ch in cat.get("channels", [])]
            cats_desc.append(f"📁 **{cat['name']}**\n└ {', '.join(ch_names[:6])}" + ("..." if len(ch_names) > 6 else ""))

        embed.add_field(name="Categories & Channels", value="\n\n".join(cats_desc[:6]) or "*None*", inline=False)
        embed.set_footer(text=f"To apply, run: s!template apply {template_id}")
        await ctx.send(embed=embed)

    @template_group.command(name="apply")
    @commands.has_permissions(administrator=True)
    async def template_apply(self, ctx: commands.Context, template_id: str, flag: Optional[str] = None):
        wipe_mode = (flag == "--wipe")
        target_data = None
        t_record = None

        if template_id in PUBLIC_TEMPLATES:
            target_data = PUBLIC_TEMPLATES[template_id]
        else:
            t_record = await ServerTemplateModel.get(self.bot.db, template_id)
            if t_record:
                target_data = t_record.get("data")

        if not target_data:
            await ctx.send("❌ Template not found! Check `s!template list` or `s!template public`.")
            return

        mode_str = "⚠️ **WIPE & APPLY** (Will delete non-bot channels and rebuild server)" if wipe_mode else "🔄 **MERGE** (Will safely create missing channels and roles)"
        confirm_embed = discord.Embed(
            title="⚠️ Confirm Template Application",
            description=f"You are about to apply template **{target_data.get('name', template_id)}** to **{ctx.guild.name}**.\n\nMode: {mode_str}\n\nAre you sure you want to proceed?",
            color=0xED4245 if wipe_mode else 0xFEE75C
        )
        view = ConfirmApplyView(ctx.author.id)
        msg = await ctx.send(embed=confirm_embed, view=view)

        await view.wait()
        if not view.confirmed:
            return

        status_msg = await ctx.send("🚀 Starting template deployment... This may take up to 60 seconds.")
        mode = "wipe" if wipe_mode else "merge"
        results = await TemplateEngine.apply_template(ctx.guild, target_data, mode=mode)

        if t_record:
            await ServerTemplateModel.increment_usage(self.bot.db, template_id)

        embed = discord.Embed(
            title="🎉 Template Applied Successfully",
            color=0x57F287,
            description=f"Template **{target_data.get('name', template_id)}** has been deployed."
        )
        embed.add_field(name="Categories Created", value=f"**{results['categories_created']}**", inline=True)
        embed.add_field(name="Channels Created", value=f"**{results['channels_created']}**", inline=True)
        embed.add_field(name="Roles Created", value=f"**{results['roles_created']}**", inline=True)
        if results["errors"]:
            embed.add_field(name="Warnings", value=f"```\n{chr(10).join(results['errors'][:5])}\n```", inline=False)
        await status_msg.edit(content=None, embed=embed)

    @template_group.command(name="export")
    @commands.has_permissions(manage_guild=True)
    async def template_export(self, ctx: commands.Context, template_id: str):
        target_data = None
        if template_id in PUBLIC_TEMPLATES:
            target_data = PUBLIC_TEMPLATES[template_id]
        else:
            t = await ServerTemplateModel.get(self.bot.db, template_id)
            if t:
                target_data = t.get("data")

        if not target_data:
            await ctx.send("❌ Template not found.")
            return

        json_str = json.dumps(target_data, indent=2)
        if len(json_str) < 1900:
            await ctx.send(f"```json\n{json_str}\n```")
        else:
            import io
            buf = io.BytesIO(json_str.encode("utf-8"))
            file = discord.File(buf, filename=f"template_{template_id}.json")
            await ctx.send(f"📄 Exported template `{template_id}`:", file=file)

    @template_group.command(name="delete")
    @commands.has_permissions(administrator=True)
    async def template_delete(self, ctx: commands.Context, template_id: str):
        if template_id in PUBLIC_TEMPLATES:
            await ctx.send("❌ Built-in public templates cannot be deleted.")
            return
        res = await ServerTemplateModel.delete(self.bot.db, template_id, ctx.guild.id)
        await ctx.send(f"🗑️ Template `{template_id}` deleted.")


async def setup(bot):
    await bot.add_cog(TemplatesCog(bot))
