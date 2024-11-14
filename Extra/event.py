import discord 
from discord.ext import commands
import aiohttp

class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        invite = await guild.text_channels[0].create_invite(
            max_age=0, max_uses=0, unique=True
        )
        
        channel_id = 1217117538689880079  
        channel = self.bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="Joined A Guild",
                description=f"**ID:** {guild.id}\n**Name:** {guild.name}\n**MemberCount:** {len(guild.members)}\n**Created:** <t:{int(guild.created_at.timestamp())}:R>",
                color=discord.Color.green()
            )
            embed.add_field(name="Invite Link", value=invite.url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        channel_id = 1217310374848630815  
        channel = self.bot.get_channel(channel_id)
        if channel:
            embed = discord.Embed(
                title="Left A Guild",
                description=f"**ID:** {guild.id}\n**Name:** {guild.name}\n**MemberCount:** {len(guild.members)}\n**Created:** <t:{int(guild.created_at.timestamp())}:R>",
                color=discord.Color.red()
            )
            await channel.send(embed=embed)


async def setup(bot):
   await bot.add_cog(Event(bot))
