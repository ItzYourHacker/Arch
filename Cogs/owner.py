from __future__ import annotations
from discord.ext import commands, menus
from discord import *
import json
import os
import discord
import aiohttp
from Extra.paginator import PaginatorView

tick = "<:IconTick:1213170250267492383>"
info = './Database/info.json'

with open("./Database/info.json", "r") as f:
    DATA = json.load(f)

OWNER_IDS = DATA["OWNER_IDS"]
No_Prefix = DATA["np"]
ADMIN = DATA["admin"]


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x38024a

   

    @commands.command(
        name="reload", help="Reload all cogs."
    )
    @commands.is_owner()
    async def _reload(self, ctx, extension):
        try:
            self.bot.unload_extension(f"cogs.{extension}")
            self.bot.load_extension(f"cogs.{extension}")
            await ctx.reply(embed=discord.Embed(title=f"<:IconTick:1213170250267492383> | Successfully Reloaded `{extension}`", color=self.color))

        except commands.ExtensionNotFound:
            await ctx.reply(embed=discord.Embed(title=f"<:crosss:1212440602659262505> | Extension `{extension}` not found.", color=self.color))
        except Exception as e:
            await ctx.reply(embed=discord.Embed(title=f"<:crosss:1212440602659262505> | Failed To Reload `{extension}`", color=self.color))
            print(e)

    @commands.command(
        name="sync", help="Syncs all databases."
    )
    @commands.is_owner()
    async def _sync(self, ctx):
        await ctx.reply("Syncing...", mention_author=False)
        with open('anti.json', 'r') as f:
            data = json.load(f)
        for guild in self.bot.guilds:
            if str(guild.id) not in data['guild']:
                data['guilds'][str(guild.id)] = 'on'
                with open('anti.json', 'w') as f:
                    json.dump(data, f, indent=4)
            else:
                pass
        with open('config.json', 'r') as f:
            data = json.load(f)
        for op in data["guilds"]:
            g = self.bot.get_guild(int(op))
            if not g:
                data["guilds"].pop(str(op))
                with open('config.json', 'w') as f:
                    json.dump(data, f, indent=4)

    @commands.group(name="admin", help="admin list management.")
    @commands.is_owner()
    async def _admin(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_admin.group(name="list", help="List of arch admins", aliases=['admins'])
    @commands.is_owner()
    async def show(self, ctx):
        with open(info, "r") as f:
            data = json.load(f)
            np_users = data.get("admin", [])  # Get the list of np_users from the data or an empty list if not present

        users_per_page = 10
        embeds = []
        user_list = [ctx.guild.get_member(user_id).mention for user_id in np_users if ctx.guild.get_member(user_id)]
        page_number = 1
        for idx in range(0, len(user_list), users_per_page):
            page_users = user_list[idx:idx + users_per_page]
            numbered_users = [f"<:icons_text1:1227261392458092635>**{idx + 1}**. {user}" for idx, user in
                              enumerate(page_users, start=idx)]
            embed = discord.Embed(title="__Arch Admin list__", description="\n".join(numbered_users),
                                  color=self.color)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Page {page_number}/{(len(user_list) // users_per_page) + 1} • Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            embeds.append(embed)
            page_number += 1

        if embeds:
            paginator = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
            await ctx.reply(embed=paginator.initial, view=paginator)
        else:
            ray = discord.Embed(title="<a:Error:1227648997389504664> | No users found")
            ray.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=ray)

    @_admin.group(name="add", help="Add user to Admin.", aliases=['giveadmin'])
    @commands.is_owner()
    async def give(self, ctx, user: discord.User):
        with open(info, 'r') as idk:
            data = json.load(idk)
        np = data["admin"]
        if user.id in np:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | The User You Provided Already In Admin list**",
                color=self.color
            )
            await ctx.reply(embed=embed)
            return
        else:
            data["admin"].append(user.id)
        with open(info, 'w') as idk:
            json.dump(data, idk, indent=4)
            embed1 = discord.Embed(
                description=f'{tick} | Added {user} to admin',
                color=self.color
            )
            await ctx.reply(embed=embed1)

    @_admin.group(name="remove", help="Remove user from Admin.", aliases=["removeadmin"])
    @commands.is_owner()
    async def readmin(self, ctx, user: discord.User):
        with open(info, 'r') as idk:
            data = json.load(idk)
        np = data["admin"]
        if user.id not in np:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | {user} is not in Admin list!**",
                color=self.color
            )
            await ctx.reply(embed=embed)
            return
        else:
            data["admin"].remove(user.id)
        with open(info, 'w') as idk:
            json.dump(data, idk, indent=4)
            embed2 = discord.Embed(
                description=f"{tick} | Removed Admin from {user} ",
                color=self.color
            )
            await ctx.reply(embed=embed2)

    @commands.group(name="np", help="No prefix list management.")
    async def _np(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_np.group(name="list", help="List users in no prefix.")
    async def list_np(self, ctx):
        if ctx.guild is None:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | This command can only be used in a server.**",
                color=self.color
            )
            return await ctx.reply(embed=embed)

        if ctx.author.id not in ADMIN and ctx.author.id not in OWNER_IDS:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | You don't have permission to use this command.**",
                color=self.color
            )
            return await ctx.reply(emebd=embed)

        with open(info, "r") as f:
            data = json.load(f)
            np_users = data.get("np", [])  # Get the list of np_users from the data or an empty list if not present

        users_per_page = 10
        embeds = []
        user_list = [ctx.guild.get_member(user_id).mention for user_id in np_users if
                     ctx.guild.get_member(user_id)]
        page_number = 1
        for idx in range(0, len(user_list), users_per_page):
            page_users = user_list[idx:idx + users_per_page]
            numbered_users = [f"<:icons_text1:1227261392458092635>**{idx + 1}**. {user}" for idx, user in
                              enumerate(page_users, start=idx)]
            embed = discord.Embed(title="__Arch NP list__", description="\n".join(numbered_users),
                                  color=self.color)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Page {page_number}/{(len(user_list) // users_per_page) + 1} • Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            embeds.append(embed)
            page_number += 1

        if embeds:
            paginator = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
            await ctx.reply(embed=paginator.initial, view=paginator)
        else:
            ray = discord.Embed(title="<a:Error:1227648997389504664> | No users found")
            ray.set_footer(text=f"{ctx.author.name}", icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=ray)

    @_np.group(name="add", help="Add user to no prefix.")
    async def add(self, ctx, user: discord.User):
        if ctx.guild is None:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | This command can only be used in a server.**",
                color=self.color
            )
            return await ctx.reply(embed=embed)

        if ctx.author.id not in ADMIN and ctx.author.id not in OWNER_IDS:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | You don't have permission to use this command.**",
                color=self.color
            )

        with open(info, 'r') as idk:
            data = json.load(idk)
        np = data["np"]
        if user.id in np:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | The User You Provided Already In My No Prefix**",
                color=self.color
            )
            await ctx.reply(embed=embed)
            return
        else:
            data["np"].append(user.id)
        with open(info, 'w') as idk:
            json.dump(data, idk, indent=4)
            embed1 = discord.Embed(
                description=f'{tick} | Added no prefix to {user} for all',
                color=self.color
            )
            await ctx.reply(embed=embed1)

    @_np.group(name="remove", help="Remove user from no prefix.", aliases=["npr"])
    async def remove(self, ctx, user: discord.User):
        if ctx.guild is None:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | This command can only be used in a server.**",
                color=self.color
            )
            return await ctx.reply(embed=embed)

        if ctx.author.id not in ADMIN and ctx.author.id not in OWNER_IDS:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | You don't have permission to use this command.**",
                color=self.color
            )

        with open(info, 'r') as idk:
            data = json.load(idk)
        np = data["np"]
        if user.id not in np:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | {user} is not in no prefix!**",
                color=self.color
            )
            await ctx.reply(embed=embed)
            return
        else:
            data["np"].remove(user.id)
        with open(info, 'w') as idk:
            json.dump(data, idk, indent=4)
            embed2 = discord.Embed(
                description=f"{tick} | Removed no prefix from {user} for all",
                color=self.color
            )
            await ctx.reply(embed=embed2)

    @commands.command(
        name="geninvite", help="Generate an invite link for the provided guild ID."
    )
    @commands.is_owner()
    async def geninvite(self, ctx, guild_id: int):
        try:
            guild = self.bot.get_guild(guild_id)
            if guild:
                invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)
                await ctx.send(f"Invite link for {guild.name}: {invite}")
            else:
                await ctx.send("Guild not found.")
        except discord.errors.Forbidden:
            embed = discord.Embed(
                description=f"**<a:Error:1227648997389504664> | I don't have permission to create invites in that guild.**",
                color=self.color
            )
            await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Owner(bot))
