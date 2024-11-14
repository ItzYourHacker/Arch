import re
import datetime
from discord.ext import commands
import discord
from typing import Union
tick="<:1209:1227285187717627904>"
class YourCogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color =  0x38024a
        self.sniped_messages = {}
    async def do_removal(self, ctx, limit, predicate):
        if limit > 2000:
            return await ctx.send(f"Too many messages to search for ({limit}/2000)")

        deleted = await ctx.channel.purge(limit=limit, check=predicate)

    @commands.group(invoke_without_command=True,
                    help="Clears the messages",
                    usage="purge <amount>",
                    aliases=['clear'])
    @commands.has_guild_permissions(manage_messages=True)
    
    async def purge(self, ctx, amount: int = 10):
        if amount > 1000:
            return await ctx.send(
                "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
            )
        deleted = await ctx.channel.purge(limit=amount + 1)
        return await ctx.send(
            f"**{tick} Deleted {len(deleted)-1} message(s)**"
        )

    @purge.command(help="Clears the messages starts with the given letters",
                   usage="purge startswith <text>")
    
    @commands.has_guild_permissions(manage_messages=True)
    async def startswith(self, ctx, key, amount: int = 10):
        if amount > 1000:
            return await ctx.send(
                "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
            )
        global counter
        counter = 0

        def check(m):
            global counter
            if counter >= amount:
                return False

            if m.content.startswith(key):
                counter += 1
                return True
            else:
                return False

        deleted = await ctx.channel.purge(limit=100, check=check)
        return await ctx.send(
            f"**{tick} Deleted {len(deleted)}/{amount} message(s) which started with the given keyword**"
        )

    @purge.command(help="Clears the messages ends with the given letter",
                   usage="purge endswith <text>")
    
    @commands.has_guild_permissions(manage_messages=True)
    async def endswith(self, ctx, key, amount: int = 10):
        if amount > 1000:
            return await ctx.send(
                "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
            )
        global counter
        counter = 0

        def check(m):
            global counter
            if counter >= amount:
                return False

            if m.content.endswith(key):
                counter += 1
                return True
            else:
                return False

        deleted = await ctx.channel.purge(limit=100, check=check)
        return await ctx.send(
            f"**{tick} Deleted {len(deleted)}/{amount} message(s) which ended with the given keyword**"
        )

    @purge.command(help="Clears the messages contains with the given argument",
                   usage="purge contains <message>")
    
    @commands.has_guild_permissions(manage_messages=True)
    async def contains(self, ctx, key, amount: int = 10):
        if amount > 1000:
            return await ctx.send(
                "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
            )
        global counter
        counter = 0

        def check(m):
            global counter
            if counter >= amount:
                return False

            if key in m.content:
                counter += 1
                return True
            else:
                return False

        deleted = await ctx.channel.purge(limit=100, check=check)
        return await ctx.send(
            f"**{tick} Deleted {len(deleted)}/{amount} message(s) which contained the given keyword**"
        )

    @purge.command(help="Clears the messages of the given user",
                   usage="purge <user>")
    
    @commands.has_guild_permissions(manage_messages=True)
    async def user(self, ctx, user: discord.Member, amount: int = 10):
        if amount > 1000:
            return await ctx.send(
                "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
            )
        global counter
        counter = 0

        def check(m):
            global counter
            if counter >= amount:
                return False

            if m.author.id == user.id:
                counter += 1
                return True
            else:
                return False

        deleted = await ctx.channel.purge(limit=100, check=check)
        return await ctx.send(
            f"**{tick} Deleted {len(deleted)}/{amount} message(s) which were sent by the mentioned user**"
        )

    @purge.command(help="Clears the messages containing invite links",
                   usage="purge invites")
    
    @commands.has_guild_permissions(manage_messages=True)
    async def invites(self, ctx, amount: int = 10):
        if amount > 1000:
            return await ctx.send(
                "Purge limit exceeded. Please provide an integer which is less than or equal to 1000."
            )
        global counter
        counter = 0

        def check(m):
            global counter
            if counter >= amount:
                return False

            if "discord.gg/" in m.content.lower():
                counter += 1
                return True
            else:
                return False

        deleted = await ctx.channel.purge(limit=100, check=check)
        return await ctx.send(
            f"**{tick} Deleted {len(deleted)}/{amount} message(s) which contained invites**"
        )
    @purge.command(description="Clears messages sent by bots in the current channel")
    @commands.has_permissions(manage_messages=True)
    async def bots(self, ctx):
        # Predicate function to check if a message was sent by a bot
        def is_bot(m):
            return m.author.bot

        # Delete messages sent by bots using the predicate function
        deleted = await ctx.channel.purge(check=is_bot)
        
        # Create and send an embed to inform about the number of deleted messages
        embed = discord.Embed(
            title="Bots Messages Deleted",
            description=f"Deleted {len(deleted)} message(s) sent by bots.",
            color=self.color
        )
        await ctx.send(embed=embed, delete_after=5)

    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        # Store deleted messages in the sniped_messages dictionary
        self.sniped_messages[message.channel.id] = message

    @commands.command(description="Snipes the most recent deleted message")
    async def snipe(self, ctx: commands.Context, *, count: int = 1):
        channel_id = ctx.channel.id
        # Check if there are any recently deleted messages in this channel
        if channel_id not in self.sniped_messages:
            return await ctx.send("There are no recently deleted messages in this channel.")

        # Retrieve the requested number of deleted messages or the last one if count is not provided
        deleted_messages = [self.sniped_messages[channel_id]] if count == 1 else list(self.sniped_messages.values())[-count:]

        for deleted_message in deleted_messages:
            # Create an embed to display the details of the deleted message
            embed = discord.Embed(title="Sniped Message",
                                  description=f"Message sent by {deleted_message.author.mention} deleted in {ctx.channel.mention}",
                                  color=self.color,
                                  timestamp=deleted_message.created_at)
            embed.add_field(name="Content:", value=deleted_message.content or "*Content Unavailable*", inline=False)
            embed.set_footer(text=f"sent By: {deleted_message.author}", icon_url=deleted_message.author.avatar.url)

            # Check if the deleted message has attachments
            if deleted_message.attachments:
                # Add attachment URLs to the embed
                attachment_urls = "\n".join(attachment.url for attachment in deleted_message.attachments)
                embed.add_field(name="Attachments:", value=attachment_urls, inline=False)

            # Send the embed to the channel where the command was invoked
            await ctx.send(embed=embed)

async def setup(bot):
   await bot.add_cog(YourCogName(bot))
