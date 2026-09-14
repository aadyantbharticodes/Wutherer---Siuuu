from __future__ import annotations

from typing import TYPE_CHECKING, Optional

import discord
from discord.ext import commands

from bot.core.cog import WuthererCog
from bot.core.context import WuthererContext
from bot.core.checks import is_admin
from bot.database.models.shop import ShopModel, ShopItem
from bot.database.models.inventory import InventoryModel
from bot.database.models.economy import EconomyModel

if TYPE_CHECKING:
    from bot.core.bot import WuthererBot


class Shop(WuthererCog, name="Shop"):

    def __init__(self, bot: WuthererBot) -> None:
        super().__init__(bot)

    @commands.group(name="shop", aliases=["store", "market"], invoke_without_command=True)
    async def shop_group(self, ctx: WuthererContext) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = ShopModel(db)
            items = await dao.list_items(ctx.guild.id)

        if not items:
            await ctx.send_warn(
                f"The shop in **{ctx.guild.name}** is currently empty.\n"
                "Staff can add items using `s!shop add role @Role <price>`."
            )
            return

        embed = self.bot.embed.create(
            title=f"🏪 Server Shop — {ctx.guild.name}",
            description="Use `s!buy <item_id>` to purchase an item with your credits.\nCheck your balance with `s!balance`.",
        )

        for itm in items:
            stock_str = "Unlimited" if itm.stock < 0 else f"{itm.stock} remaining"
            role_mention = f"<@&{itm.role_id}>" if itm.role_id else ""
            desc = (
                f"• **Price:** `🪙 {itm.price:,} credits`\n"
                f"• **Stock:** `{stock_str}`\n"
                f"• **Type:** `{itm.item_type.capitalize()}` {role_mention}\n"
                f"• *{itm.description}*\n"
            )
            embed.add_field(name=f"ID `#{itm.item_id}`: {itm.name}", value=desc, inline=False)

        embed.set_footer(text="Earn credits with s!daily, s!work, and mini-games!")
        await ctx.send(embed=embed)

    @shop_group.command(name="add")
    @is_admin()
    async def shop_add(
        self,
        ctx: WuthererContext,
        item_type: str,
        target: str,
        price: int,
        *,
        description: Optional[str] = None,
    ) -> None:
        if price <= 0:
            await ctx.send_error("Item price must be greater than zero.")
            return

        role_id = None
        item_name = target
        desc = description or "No description provided."

        if item_type.lower() == "role":
            try:
                role = await commands.RoleConverter().convert(ctx, target)
                role_id = role.id
                item_name = role.name
            except commands.BadArgument:
                await ctx.send_error(f"Could not find role: `{target}`")
                return

        async with self.bot.db_pool.acquire() as db:
            dao = ShopModel(db)
            item_id = await dao.add_item(
                guild_id=ctx.guild.id,
                name=item_name,
                description=desc,
                price=price,
                item_type=item_type.lower(),
                role_id=role_id,
            )

        await ctx.send_success(
            f"Added **{item_name}** to the shop for `🪙 {price:,}` credits! (ID: `#{item_id}`)"
        )

    @shop_group.command(name="delete", aliases=["remove"])
    @is_admin()
    async def shop_delete(self, ctx: WuthererContext, item_id: int) -> None:
        async with self.bot.db_pool.acquire() as db:
            dao = ShopModel(db)
            deleted = await dao.delete_item(item_id, ctx.guild.id)

        if deleted:
            await ctx.send_success(f"Item `#{item_id}` has been removed from the shop.")
        else:
            await ctx.send_error(f"Item `#{item_id}` was not found in this guild's shop.")

    @commands.command(name="buy", aliases=["purchase"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy_item(self, ctx: WuthererContext, item_id: int) -> None:
        async with self.bot.db_pool.acquire() as db:
            shop_dao = ShopModel(db)
            econ_dao = EconomyModel(db)
            inv_dao = InventoryModel(db)

            item = await shop_dao.get_item(item_id, ctx.guild.id)
            if not item or not item.enabled:
                await ctx.send_error(f"Item `#{item_id}` is not available in the shop.")
                return

            if item.stock == 0:
                await ctx.send_warn(f"**{item.name}** is currently out of stock!")
                return


            user_balance = await econ_dao.get_wallet(ctx.guild.id, ctx.author.id)
            if user_balance < item.price:
                shortfall = item.price - user_balance
                await ctx.send_error(
                    f"Insufficient credits. You need `🪙 {item.price:,}` credits, but you only have `🪙 {user_balance:,}`.\n"
                    f"You are short by `🪙 {shortfall:,}` credits."
                )
                return


            if item.item_type == "role" and item.role_id:
                role = ctx.guild.get_role(item.role_id)
                if not role:
                    await ctx.send_error("The role associated with this item no longer exists on the server.")
                    return
                if role in ctx.author.roles:
                    await ctx.send_warn(f"You already possess the {role.mention} role!")
                    return
                try:
                    await ctx.author.add_roles(role, reason=f"Sentinel Shop Purchase: #{item.item_id}")
                except discord.Forbidden:
                    await ctx.send_error("I lack permission to assign that role (my role must be higher in hierarchy).")
                    return


            await econ_dao.modify_wallet(ctx.guild.id, ctx.author.id, -item.price)


            await inv_dao.add_item(
                guild_id=ctx.guild.id,
                user_id=ctx.author.id,
                item_id=item.item_id,
                item_name=item.name,
                item_type=item.item_type,
                quantity=1,
            )


            if item.stock > 0:
                await shop_dao.decrement_stock(item.item_id)

        await ctx.send_success(
            f"🎉 Congratulations! You purchased **{item.name}** for `🪙 {item.price:,}` credits."
        )

    @commands.command(name="inventory", aliases=["inv", "bag"])
    async def inventory_cmd(self, ctx: WuthererContext, *, member: Optional[discord.Member] = None) -> None:
        target = member or ctx.author
        async with self.bot.db_pool.acquire() as db:
            dao = InventoryModel(db)
            items = await dao.get_user_inventory(ctx.guild.id, target.id)

        if not items:
            msg = "Your inventory is currently empty. Visit `s!shop` to purchase items!" if target == ctx.author else f"{target.display_name}'s inventory is empty."
            await ctx.send_warn(msg)
            return

        embed = self.bot.embed.create(
            title=f"🎒 Inventory — {target.display_name}",
            description=f"Showing `{len(items)}` unique item types owned.",
        )
        embed.set_thumbnail(url=target.display_avatar.url)

        for itm in items:
            acquired_ts = f"<t:{itm.acquired_at}:R>"
            embed.add_field(
                name=f"{itm.item_name} (x{itm.quantity})",
                value=f"• **Type:** `{itm.item_type}`\n• **Acquired:** {acquired_ts}\n• **Item ID:** `#{itm.item_id}`",
                inline=True,
            )

        embed.set_footer(text="Use s!gift <@member> <item_id> to share items with friends!")
        await ctx.send(embed=embed)

    @commands.command(name="gift", aliases=["giveitem"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gift_item(self, ctx: WuthererContext, member: discord.Member, item_id: int) -> None:
        if member == ctx.author:
            await ctx.send_error("You cannot gift items to yourself.")
            return

        if member.bot:
            await ctx.send_error("Bots cannot receive inventory items.")
            return

        async with self.bot.db_pool.acquire() as db:
            dao = InventoryModel(db)
            inventory = await dao.get_user_inventory(ctx.guild.id, ctx.author.id)
            matching = next((i for i in inventory if i.item_id == item_id), None)

            if not matching or matching.quantity < 1:
                await ctx.send_error(f"You do not possess item `#{item_id}` in your inventory.")
                return


            success = await dao.transfer_item(
                guild_id=ctx.guild.id,
                sender_id=ctx.author.id,
                recipient_id=member.id,
                item_id=item_id,
                item_name=matching.item_name,
                item_type=matching.item_type,
                quantity=1,
            )

        if success:
            await ctx.send_success(
                f"🎁 You successfully gifted **{matching.item_name}** to {member.mention}!"
            )
        else:
            await ctx.send_error("Item transfer could not be completed.")


async def setup(bot: WuthererBot) -> None:
    await bot.add_cog(Shop(bot))

