from ast import literal_eval
from cmath import e
from glob import iglob
import discord
from discord.ext import commands
from discord import Webhook
import typing
from typing import Union, Optional
import re
import sqlite3
import asyncio
from collections import Counter
import aiohttp
import datetime
import requests
import random
from io import BytesIO
import matplotlib
from Extra.paginator import PaginatorView



error="<a:error:1227648997389504664>"
tick="<:1209:1227285187717627904>"

xd = {}
async def getchannel(guild_id):
    if guild_id not in xd:
        return 0
    else:
        return xd[guild_id]

async def updatechannel(guild_id, channel_id):
    xd[guild_id] = channel_id
    return True

async def delchannel(guild_id):
    del xd[guild_id]
    return True


class BasicView(discord.ui.View):
    def __init__(self, ctx: commands.Context, timeout = 60):
        super().__init__(timeout=timeout)
        self.ctx = ctx

    

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [1043194242476036107]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True
class channeldropdownmenu(discord.ui.ChannelSelect):
    def __init__(self, ctx: commands.Context):
        super().__init__(placeholder="Select channel",
            min_values=1,
            max_values=1,
            channel_types=[discord.ChannelType.text]
        )
        self.ctx = ctx
    
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=False)
        await updatechannel(self.ctx.guild.id, self.values[0].id)
        self.view.stop()

class channelmenuview(discord.ui.View):
    def __init__(self, ctx: commands.Context):
        super().__init__(timeout=None)
        self.ctx = ctx
        self.value = None
        self.add_item(channeldropdownmenu(self.ctx))

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id and interaction.user.id not in  [1043194242476036107]:
            await interaction.response.send_message(f"Um, Looks like you are not the author of the command...", ephemeral=True)
            return False
        return True


class xddd(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="All", style=discord.ButtonStyle.gray)
    async def a(self, interaction, button):
        self.value = 'all'
        self.stop()
    @discord.ui.button(label="Server update", style=discord.ButtonStyle.gray)
    async def server(self, interaction, button):
        self.value = 'update'
        self.stop()
    @discord.ui.button(label="Ban", style=discord.ButtonStyle.gray)
    async def _b(self, interaction, button):
        self.value = 'ban'
        self.stop()
    @discord.ui.button(label="Kick", style=discord.ButtonStyle.gray)
    async def _k(self, interaction, button):
        self.value = 'kick'
        self.stop()

class channeloption(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    @discord.ui.button(label="Text", style=discord.ButtonStyle.gray)
    async def a(self, interaction, button):
        self.value = 'text'
        self.stop()
    @discord.ui.button(label="Voice", style=discord.ButtonStyle.gray)
    async def server(self, interaction, button):
        self.value = 'voice'
        self.stop()
    @discord.ui.button(label="Category", style=discord.ButtonStyle.gray)
    async def _b(self, interaction, button):
        self.value = 'category'
        self.stop()

class nice(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="1", style=discord.ButtonStyle.gray)
    async def _one(self, interaction, button):
        self.value = 1
        self.stop()
    @discord.ui.button(label="10", style=discord.ButtonStyle.gray)
    async def _two(self, interaction, button):
        self.value = 10
        self.stop()
    @discord.ui.button(label="20", style=discord.ButtonStyle.gray)
    async def _third(self, interaction, button):
        self.value = 20
        self.stop()
    @discord.ui.button(label="100", style=discord.ButtonStyle.gray)
    async def _four(self, interaction, button):
        self.value = 100
        self.stop()
    @discord.ui.button(label="Custom", style=discord.ButtonStyle.gray)
    async def _five(self, interaction, button):
        self.value = "custom"
        self.stop()

class OnOrOff(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=60)
        self.value = None

    

    @discord.ui.button(emoji="<:IconTick:1213170250267492383> ", custom_id='Yes', style=discord.ButtonStyle.green)
    async def dare(self, interaction, button):
        self.value = 'Yes'
        self.stop()

    @discord.ui.button(emoji="<:crosss:1212440602659262505> ", custom_id='No', style=discord.ButtonStyle.danger)
    async def truth(self, interaction, button):
        self.value = 'No'
        self.stop()

class create(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="Users only", custom_id='users', style=discord.ButtonStyle.green)
    async def users(self, interaction, button):
        self.value = 'users'
        self.stop()
    @discord.ui.button(label="Bots Only", custom_id='bots', style=discord.ButtonStyle.green)
    async def bots(self, interaction, button):
        self.value = 'bots'
        self.stop()

    @discord.ui.button(label="Both", custom_id='both', style=discord.ButtonStyle.danger)
    async def both(self, interaction, button):
        self.value = 'both'
        self.stop()

class night(BasicView):
    def __init__(self, ctx: commands.Context):
        super().__init__(ctx, timeout=120)
        self.value = None

    

    @discord.ui.button(label="Simple Roles Only", custom_id='simple', style=discord.ButtonStyle.green)
    async def simple(self, interaction, button):
        self.value = 'simple'
        self.stop()
    @discord.ui.button(label="Bot Roles Only", custom_id='bot', style=discord.ButtonStyle.green)
    async def bot(self, interaction, button):
        self.value = 'bot'
        self.stop()

    @discord.ui.button(label="Both", custom_id='both', style=discord.ButtonStyle.danger)
    async def both(self, interaction, button):
        self.value = 'both'
        self.stop()

def convert(date):
    date.replace("second", "s")
    date.replace("seconds", "s")
    date.replace("minute", "m")
    date.replace("minutes", "m")
    date.replace("hour", "h")
    date.replace("hours", "h")
    date.replace("day", "d")
    date.replace("days", "d")
    pos = ["s", "m", "h", "d"]
    time_dic = {"s": 1, "m": 60, "h": 3600, "d": 3600 *24}
    i = {"s": "Secondes", "m": "Minutes", "h": "Heures", "d": "Jours"}
    unit = date[-1]
    if unit not in pos:
        return -1
    try:
        val = int(date[:-1])

    except:
        return -2

    if val == 1:
        return val * time_dic[unit], i[unit][:-1]
    else:
        return val * time_dic[unit], i[unit]



class moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.role_status = {}
        self.bot.rrole_status = {}
        self.color = 0x38024a
    
    
        
    
    
    
    @commands.command(description="Changes the icon for the role")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def roleicon(self, ctx: commands.Context, role: discord.Role, *, icon: Union[discord.Emoji, discord.PartialEmoji, str]=None):
        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
        if ctx.author.top_role.position <= role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position from your top role!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if icon is None:
            c = False
            url = None
            for xd in ctx.message.attachments:
                url = xd.url
                c = True
            if c:
                try:
                    async with aiohttp.request("GET", url) as r:
                        img = await r.read()
                        await role.edit(display_icon=img)
                    em = discord.Embed(description=f"Successfully changed icon of {role.mention}", color=self.color)
                except:
                    return await ctx.reply("Failed to change the icon of the role")
            else:
                await role.edit(display_icon=None)
                em = discord.Embed(description=f"Successfully removed icon from {role.mention}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        if isinstance(icon, discord.Emoji) or isinstance(icon, discord.PartialEmoji):
            png = f"https://cdn.discordapp.com/emojis/{icon.id}.png"
            try:
              async with aiohttp.request("GET", png) as r:
                img = await r.read()
            except:
              return await ctx.reply("Failed to change the icon of the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"Successfully changed the icon for {role.mention} to {icon}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        else:
            if not icon.startswith("https://"):
                return await ctx.reply("Give a valid link")
            try:
              async with aiohttp.request("GET", icon) as r:
                img = await r.read()
            except:
              return await ctx.reply("An error occured while changing the icon for the role")
            await role.edit(display_icon=img)
            em = discord.Embed(description=f"Successfully changed the icon for {role.mention}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)

   

    @commands.command(description="Enables slowmode for the channel")
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, *, time=None):
        if time is None:
            await ctx.channel.edit(slowmode_delay=None, reason=f"Slowmode edited by {str(ctx.author)}")
            em = discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully removed slowmode for channel {ctx.channel.mention}", color=0x00f7ff)
            return await ctx.channel.send(embed=em)
        t = "".join([ch for ch in time if ch.isalpha()])
        num = 0
        for c in time:
            if c.isdigit():
                num = num + int(c)
        if t == '':
            num = num
        elif t == 's' or t == 'seconds' or t == 'second':
            num = num
        elif t == 'm' or t == 'minutes' or t == 'minute':
            num = num*60
        elif t == 'h' or t == 'hours' or t == 'hour':
            num = num*60*60
        else:
            return await ctx.reply("Invalid time")
        try:
            await ctx.channel.edit(slowmode_delay=num, reason=f"Slowmode edited by {str(ctx.author)}")
        except:
            return await ctx.reply("Invalid time")
        em = discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully changed slowmode for channel {ctx.channel.mention} to {t} seconds", color=0x00f7ff)
        await ctx.channel.send(embed=em)

    @commands.command(usage="[#channel/id]", name="lock", description="Locks the channel")
    @commands.has_permissions(administrator=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Locked Channel", color=self.color)
        em.set_author(name="Channel Locked", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)

    @commands.command(description="locks all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def lockall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Lock all the channels of the Server", color=self.color)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels ran by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Locked All Channel", color=self.color)
            em.set_author(name="All Channel Locked", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)        

    @commands.command(usage="[#channel/id]", name="unlock", description="Unlocks the channel")
    @commands.has_permissions(administrator=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Unlocked Channel", color=self.color)
        em.set_author(name="Channel Unlocked", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Unlocks all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def unlockall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unlock all the channels of the Server", color=self.color)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.send_messages = True
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels ran by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Unlocked All Channel", color=self.color)
            em.set_author(name="All Channel Unlocked", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.command(description="Hides the channel")
    @commands.has_permissions(administrator=True)
    async def hide(self, ctx, channel: discord.abc.GuildChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Hidden Channel", color=self.color)
        em.set_author(name="Channel Hidden", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Hide all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def hideall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Hide all the channels of the Server", color=self.color)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = False
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels ran by {ctx.author}")
            em = discord.Embed(description=f"Succesfully Hidden Channel", color=self.color)
            em.set_author(name="Channel Hidden", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        
    @commands.command(description="Unhides the channel")
    @commands.has_permissions(administrator=True)
    async def unhide(self, ctx, channel: discord.abc.GuildChannel = None, *, reason = None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.view_channel = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        em = discord.Embed(description=f"Succesfully Unhidden Channel", color=self.color)
        em.set_author(name="Channel Unhidden", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.reply(embed=em)
    
    @commands.command(description="Unhide all channels in the server")
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    async def unhideall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unhide all the channels of the Server", color=self.color)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            await test.delete()
            return await ctx.reply(content="Timed out!", mention_author=False)
        if view.value == 'Yes':
            await test.delete()
            for channel in ctx.guild.channels:
                overwrite = channel.overwrites_for(ctx.guild.default_role)
                overwrite.view_channel = True
            
                await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Lock all channels ran by {ctx.author}")
                em = discord.Embed(description=f"Succesfully Unhidden All Channel", color=self.color)
                em.set_author(name="All Channel Unhidden", icon_url=ctx.author.display_avatar.url)
                em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)


    @commands.command(name='enlarge', description='Enlarges an emoji.')
    async def enlarge(self, ctx, emoji: Union[discord.Emoji, discord.PartialEmoji, str]):
        if isinstance(emoji, discord.Emoji):
            await ctx.send(emoji.url)
        elif isinstance(emoji, discord.PartialEmoji):
            await ctx.send(emoji.url)
        elif isinstance(emoji, str) and not emoji.isalpha() and not emoji.isdigit():
            await ctx.send(emoji)

    
    @commands.command(description="Created a role in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def addrole(self, ctx, color, *,name):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        try:
            color = matplotlib.colors.cnames[color.lower()]
        except:
            color = color
        color = str(color).replace("#", "")
        try:
            color = int(color, base=16)
        except:
            return await ctx.reply(f"Provide a specific color")
        role = await ctx.guild.create_role(name=name, color=color, reason=f"Role created by {str(ctx.author)}")
        em = discord.Embed(description=f"Created {role.mention} role", color=self.color)
        await ctx.reply(embed=em, mention_author=False)
        
    @commands.command(description="Deletes a role in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def delrole(self, ctx, *,role:discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        if role.position >= ctx.guild.me.top_role.position:
                em = discord.Embed(description=f"{role.mention} is above my top role, move my role above the {role.mention} and run the command again", color=self.color)
                return await ctx.reply(embed=em, mention_author=False)
        await role.delete()
        await ctx.reply(embed=discord.Embed(description="Successfully deleted the role", color=self.color), mention_author=False)
    
    @commands.group(
        invoke_without_command=True,
        description="Adds a role to the user"
    )
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role(self, ctx, user: discord.Member, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position from your top role!", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        if role in user.roles:
            await user.remove_roles(role, reason=f"Role removed by {ctx.author.name}")
            em=discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully removed {role.mention} from {user.mention}", color=ctx.author.color)
            return await ctx.send(embed=em)
        await user.add_roles(role, reason=f"Role given by {ctx.author.name}")
        em=discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully Given {role.mention} to {user.mention}", color=ctx.author.color)
        await ctx.reply(embed=em)

    @role.command(name="all", description="Gives a role to all the members in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_all(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a add role process is running", color=self.color)
                return await ctx.send(embed=em)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if not role in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the members of the server", color=self.color))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Members?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(test)} Members**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for member in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await member.add_roles(role, reason=f"Role all ran by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} members out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Given __{role.mention}__ to {total_count} Members**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="bots", description="Gives a role to all the bots in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_bots(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a add role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the bots of the server", color=self.color))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Bots?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(set(test))} Bots**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for bot_members in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await bot_members.add_roles(role, reason=f"Role bots ran by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} Bots out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Given __{role.mention}__ to {total_count} Bots**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="humans", description="Gives a role to all the users in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_humans(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a add role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([not member.bot, not role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already given to all the users of the server", color=self.color))
        emb=discord.Embed(description=f"Do you want to give __{role.mention}__ to {len(test)} Users?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.role_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Giving __{role.mention}__ to {len(set(test))} Users**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for humans in test:
            if self.bot.role_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.role_status[ctx.guild.id]
                self.bot.role_status[ctx.guild.id] = (count+1, len(test), True)
                await humans.add_roles(role, reason=f"Role humans ran by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Giving role | Given __{role.mention}__ to {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Given __{role.mention}__ to {total_count} Users**", color=ctx.author.color)
        self.bot.role_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @role.command(name="status", description="Shows the status of current adding role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_status(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        count, total_count, sts = self.bot.role_status[ctx.guild.id]
        em = discord.Embed(description=f"Given roles to {count} users out of {total_count} users ({count/total_count * 100.0}%) of adding roles to {total_count} users", color=self.color)
        em.set_footer(text=f"{str(self.bot.user)} Adding role", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=em)

    @role.command(name="cancel", description="Cancel the current adding role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def role_cancel(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.role_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No add role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        self.bot.role_status[ctx.guild.id] = None
        
    @commands.group(
        invoke_without_command=True,
        aliases=["removerole"], description="Removes a role from the user"
    )
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole(self, ctx, user: discord.Member, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if not role in user.roles:
            em = discord.Embed(description=f'<:crosss:1212440602659262505>  The member do not has this role!', color=self.color)
            return await ctx.send(embed=em, delete_after=15)
            
        if role == ctx.author.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same position as your top role!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        await user.remove_roles(role, reason=f"role removed by {ctx.author.name}")
        em=discord.Embed(description=f"<:IconTick:1213170250267492383>  Successfully Removed {role.mention} From {user.mention}", color=ctx.author.color)
        await ctx.send(embed=em)

    @rrole.command(name="all", description="Removes a role from all the members in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_all(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a remove role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if role in member.roles]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the members of the server", color=self.color))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Members?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(test)} Members**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for member in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await member.remove_roles(role, reason=f"Rrole all ran by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Removed __{role.mention}__ from {total_count} Members**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="bots", description="Removes a role from all the bots in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_bots(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a remove role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the bots of the server", color=self.color))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Bots?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(set(test))} Bots**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for bot_members in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await bot_members.remove_roles(role, reason=f"Rrole bots ran by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Bots out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Removed __{role.mention}__ from {total_count} Bots**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="humans", description="Removes a role from all the users in the server")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_humans(self, ctx, *,role: discord.Role):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Already a remove role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
            pass
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:        
            if role.position >= ctx.author.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  That role has the same or higher position as your top role!", color=self.color)
                return await ctx.send(embed=em, delete_after=15)

        if role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  This role is higher than my role, move it to the top!", color=self.color)
            return await ctx.send(embed=em, delete_after=15)
        if role.is_bot_managed() or role.is_premium_subscriber():
            return await ctx.reply("It is a integrated role. Please provide a different role", delete_after=15)
        if not role.is_assignable():
            return await ctx.reply("I cant assign this role to anyone so please check my permissions and position.", delete_after=15)
        test = [member for member in ctx.guild.members if all([not member.bot, role in member.roles])]
        if len(test) == 0:
            return await ctx.reply(embed=discord.Embed(description=f"{role.mention} is already removed from all the users of the server", color=self.color))
        emb=discord.Embed(description=f"Do you want to remove __{role.mention}__ from {len(test)} Users?", color=ctx.author.color)
        v = OnOrOff(ctx)
        init = await ctx.send(embed=emb, view=v)
        await v.wait()
        if v.value == 'Yes':
            pass
        else:
            return await init.delete()
        self.bot.rrole_status[ctx.guild.id] = (0, len(test), True)
        em=discord.Embed(description=f"**<a:loading:988108755768062033>  |  Removing __{role.mention}__ from {len(set(test))} Users**", color=ctx.author.color)
        await init.edit(embed=em, view=None)
        for humans in test:
            if self.bot.rrole_status[ctx.guild.id] is not None:
                count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
                self.bot.rrole_status[ctx.guild.id] = (count+1, len(test), True)
                await humans.remove_roles(role, reason=f"Rrole humans ran by {ctx.author.name}")
        if count+1 != total_count:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Cancelled the process of Removing role | Removed __{role.mention}__ from {count+1} Users out of {total_count}**", color=ctx.author.color)
        else:
            em1=discord.Embed(description=f"**<:IconTick:1213170250267492383>  |  Removed __{role.mention}__ from {total_count} Users**", color=ctx.author.color)
        self.bot.rrole_status[ctx.guild.id] = None
        await init.delete()
        try:
            await ctx.reply(embed=em1)
        except:
            await ctx.send(embed=em1)

    @rrole.command(name="status", description="Shows the status of current remove role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_status(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        count, total_count, sts = self.bot.rrole_status[ctx.guild.id]
        em = discord.Embed(description=f"Removed roles from {count} users out of {total_count} users ({count/total_count * 100.0}%) of removing roles to {total_count} users", color=self.color)
        em.set_footer(text=f"{str(self.bot.user)} Removing roles", icon_url=self.bot.user.display_avatar.url)
        await ctx.send(embed=em)

    @rrole.command(name="cancel", description="Cancel the current Remove role process")
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def rrole_cancel(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        try:
            if self.bot.rrole_status[ctx.guild.id] is None:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        except:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  No remove role process is running", color=self.color)
                return await ctx.send(embed=em, delete_after=15)
        self.bot.rrole_status[ctx.guild.id] = None
        em = discord.Embed(description="Succesfully Cancelled the process", color=self.color)
        await ctx.send(embed=em)

    @commands.command(aliases=["mute"], description="Timeouts a user for specific time\nIf you don't provide the time the user will be timeout for 5 minutes")
    @commands.bot_has_guild_permissions(manage_roles=True)
    @commands.has_permissions(manage_roles=True)
    async def timeout(self, ctx, member: discord.Member, *, time= None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Your Top role should be above the top role of {str(member)}", color=self.color)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot mute owner of the server", color=self.color)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        if member.top_role.position > ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        if time is None:
            time = "5m"
        converted_time = convert(time)
        if converted_time == -1 or converted_time == -2:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Provide specific time!", color=self.color)
            return await ctx.send(embed=em)
        timeout_until = discord.utils.utcnow() + datetime.timedelta(seconds=converted_time[0])
        await member.edit(timed_out_until=timeout_until, reason=f"Muted by {ctx.author}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Muted.", color=self.color)
        em.set_author(name="Successfully Muted", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        em = discord.Embed(description=f'YOU HAVE BEEN MUTED FROM {ctx.guild.name}', color=self.color)
        em.set_footer(text=f'Muted by {ctx.author.name}')
        return await member.send(embed=em)

    @commands.command(description="Removes the timeout from the user")
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, *,member: discord.Member):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Your Top role should be above the top role of {str(member)}", color=self.color)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot unmute owner of the server", color=self.color)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        guild = ctx.guild
        await member.edit(timed_out_until=None, reason=f"Unmuted by {ctx.author}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Unmuted.", color=self.color)
        em.set_author(name="Successfully Unmuted", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        em = discord.Embed(description=f'YOU HAVE BEEN UNMUTED FROM {ctx.guild.name}', color=self.color)
        em.set_footer(text=f'Unmuted by {ctx.author.name}')
        return await member.send(embed=em)

    @commands.command(aliases=["setnick"], description="Changes the user's nickname for the server")
    @commands.has_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def nick(self, ctx, member : discord.Member, *, Name=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:

            if ctx.author.top_role.position <= member.top_role.position:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Your Top role should be above the top role of {str(member)}", color=self.color)
                return await ctx.reply(embed=em, mention_author=False)
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot change nick of owner of the server", color=self.color)
            return await ctx.send(embed=em)
        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        if Name is None:
            await member.edit(nick=None, reason=f"Nickname changed by {ctx.author.name}")
            em = discord.Embed(description=f"Successfully cleared nickname of {str(member)}", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
        if Name is not None:
            await member.edit(nick=Name, reason=f"Nickname changed by {ctx.author.name}")
            em = discord.Embed(description=f"{member} ( ID: {member.id} ) was successfully Renamed.", color=self.color)
            em.set_author(name="Successfully Changed Nick", icon_url=ctx.author.display_avatar.url)
            em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
            return await ctx.reply(embed=em, mention_author=False)

    @commands.command(description="Kicks a member from the server")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than me To run This command", color=self.color)
                return await ctx.send(embed=em)
            
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot kick owner of the server", color=self.color)
            return await ctx.send(embed=em)

        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        rs = "No Reason Provided."

        if reason:
            rs = str(reason)[:500]

        await member.kick(reason=f"Kicked by {ctx.author.name} for {reason}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully kicked.", color=self.color)
        em.set_author(name="Successfully Kicked", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:logging:1214606283953410088> Reason", value=f"{rs}", inline=True)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        if reason:
            await member.send(embed=discord.Embed(description=f'You have been kicked from **{ctx.guild.name}** with the reason: `{rs}`', color=self.color))
        else:
            await member.send(embed=discord.Embed(description=f'You have been kicked from **{ctx.guild.name}**', color=self.color))


    @commands.command(description="Unbans a member from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unban(self, ctx: commands.Context, user: discord.User):
        async for x in ctx.guild.bans():
            if x.id == user.id:
                await ctx.guild.unban(user, reason=f"Unbanned by {ctx.author.name}")
                return await ctx.send(f'<:IconTick:1213170250267492383>  Unbanned **{str(user)}**!')
        await ctx.send(f'**{str(user)}** is not banned!')
    
    @commands.command(description="Unban all the banned members in the server")
    @commands.cooldown(1, 120, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def unbanall(self, ctx):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  []:
                em = discord.Embed(description=f"<:crosss:1212440602659262505> You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        xd = [member async for member in ctx.guild.bans()]
        if len(xd) == 0:
            return await ctx.send("No Banned Users")
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Unban {len(xd)} Users", color=self.color)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            return await test.edit(content="Timed out!", view=None)
        if view.value == 'Yes':
            await test.delete()
            count = 0
            async for member in ctx.guild.bans():
                await ctx.guild.unban(member.user, reason=f"Unbaned by {ctx.author.name}")
                count+=1
        em = discord.Embed(description=f"Succesfully Unbanned All.", color=self.color)
        em.set_author(name="Successfully Unbanned All", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        return await ctx.reply(embed=em, mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
    @commands.command(description="Bans the user from the server")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
            
        if member.id == ctx.guild.owner.id:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  Idiot! You cannot ban owner of the server", color=self.color)
            return await ctx.send(embed=em)

        if ctx.guild.me.top_role.position == member.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is same as of {str(member)}!", color=self.color)
            return await ctx.send(embed=em)

        if member.top_role.position >= ctx.guild.me.top_role.position:
            em = discord.Embed(description=f"<:crosss:1212440602659262505>  My highest role is below {str(member)}!", color=self.color)
            return await ctx.send(embed=em)
        await member.ban(reason=f"Banned by {ctx.author.name} for {reason}")
        em = discord.Embed(description=f"[{member}](https://discord.com/users/{member.id}) ( ID: {member.id} ) was successfully Banned.", color=self.color)
        em.set_author(name="Successfully Banned", icon_url=ctx.author.display_avatar.url)
        em.add_field(name="<:logging:1214606283953410088> Reason", value=f"{reason}", inline=True)
        em.add_field(name="<:IconTick:1213170250267492383> Moderator", value=f"{ctx.author.mention} ( ID: {ctx.author.id} )", inline=True)
        await ctx.channel.send(embed=em)
        await member.send(embed=discord.Embed(description=f'You Have Been Banned From **{ctx.guild.name}** For The Reason: `{reason}`', color=self.color))

    @commands.command(aliases=['nuke', 'clonechannel'], description="Clones the channel")
    @commands.cooldown(1, 15, commands.BucketType.guild)
    @commands.has_permissions(administrator=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def clone(self, ctx, channel: discord.TextChannel = None):
        if ctx.guild.owner.id == ctx.author.id:
            pass
        else:
            if ctx.author.top_role.position <= ctx.guild.me.top_role.position and ctx.author.id not in  [1043194242476036107]:
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You must Have Higher Role than Bot To run This Command", color=self.color)
                return await ctx.send(embed=em)
        if channel == None:
            channel = ctx.channel
        view = OnOrOff(ctx)
        em = discord.Embed(description=f"Would You Like To Clone {channel.mention} Channel", color=self.color)
        try:
            em.set_author(name=str(ctx.author), icon_url=ctx.author.display_avatar.url)
        except:
            em.set_author(name=str(ctx.author))
        test = await ctx.reply(embed=em, view=view)
        await view.wait()
        if not view.value:
            return await test.edit(content="Timed out!", view=None)
        if view.value == 'Yes':
            await test.delete()
            channel_position = channel.position
            new = await channel.clone(reason=f"Channel nuked by {ctx.author.name}")
            await channel.delete(reason=f"Channel nuked by {ctx.author.name}")
            await new.edit(sync_permissions=True, position=channel_position)
            return await new.send(f"{ctx.author.mention}", embed=discord.Embed(title="Channel Nuked", description=f"<:IconTick:1213170250267492383> Channel has been nuked by {ctx.author.mention}.", color=self.color), mention_author=False)
        if view.value == 'No':
            await test.delete()
            em = discord.Embed(description="Canceled The Command", color=self.color)
            return await ctx.reply(embed=em, mention_author=False)
    
async def setup(bot):
    await bot.add_cog(moderation(bot))
