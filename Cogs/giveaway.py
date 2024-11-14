import discord
import asyncio
import json
import random
from discord.ext import commands
from datetime import timedelta
emoji = '<a:Giveaway:1221844411051278388>'

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.giveaway_data = {}
        self.history_file = './Database/history.json'
        self.giveaway_file = '/Database/giveaway.json'

    @commands.group(name='Giveaway', aliases=['g'])
    async def _giveaway(self, ctx: commands.Context):
        if ctx.subcommand_passed is None:
            embed = discord.Embed(
                title="Giveaway Command Help",
                description="Here are the available subcommands for the giveaway command:**```- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```**",
                color=discord.Color.blue()
            )
            embed.add_field(name="`$Giveaway start`", value="To start a giveaway", inline=False)
            embed.add_field(name="`$Giveaway reroll `", value="To reroll giveaway", inline=False)
            embed.add_field(name="`$Giveaway history`", value="To check giveaway history", inline=False)
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.load_giveaway_data()

    async def load_giveaway_data(self):
        try:
            with open(self.giveaway_file, 'r') as file:
                self.giveaway_data = json.load(file)
        except FileNotFoundError:
            self.giveaway_data = {}

    async def save_giveaway_data(self):
        with open(self.giveaway_file, 'w') as file:
            json.dump(self.giveaway_data, file)

    async def save_giveaway_history(self, guild_id, giveaway_data):
        try:
            with open(self.history_file, 'r') as file:
                history_data = json.load(file)
        except FileNotFoundError:
            history_data = {}

        if guild_id not in history_data:
            history_data[guild_id] = []

        history_data[guild_id].append(giveaway_data)

        with open(self.history_file, 'w') as file:
            json.dump(history_data, file)

    async def convert_time(self, time_str):
        if time_str[-1] == 's':
            return int(time_str[:-1])
        elif time_str[-1] == 'm':
            return int(time_str[:-1]) * 60
        elif time_str[-1] == 'h':
            return int(time_str[:-1]) * 3600
        elif time_str[-1] == 'd':
            return int(time_str[:-1]) * 86400
        else:
            return int(time_str)

    async def has_admin_permissions(self, ctx):
        return ctx.author.guild_permissions.administrator

    @_giveaway.command()
    async def start(self, ctx, duration: str, winners: int, *, prize: str):
        if not await self.has_admin_permissions(ctx):
            return await ctx.send("You do not have enough permissions to use this command.")

        duration_seconds = await self.convert_time(duration)
        guild_id = ctx.guild.id

        embed = discord.Embed(title=f"{emoji} **Giveaway** {emoji}", description=f" **React with {emoji} to participate and win** `{prize}`\n───────────────────────────\n **`Hosted by`** {ctx.author.mention}",
                              color=0x410142)
        embed.set_image(url='https://cdn.discordapp.com/attachments/1210268753036705882/1221852115304185969/divider.png?ex=66141575&is=6601a075&hm=cf2b18e95b792252568ae8d899ae4a5e605e7a5b687a4ad79a80d8508fa6bca7&')
        embed.add_field(name="**Number of Winners**", value=f"`{winners}`")
        embed.set_footer(text=f'Hosted by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/1216744904898646200/1221869676720685157/Giveaway-Header.png?ex=661425d0&is=6601b0d0&hm=ad44e38453a0b59783b1b087&')
        message = await ctx.send(embed=embed)
        await message.add_reaction(emoji)

        # Storing giveaway data
        if guild_id not in self.giveaway_data:
            self.giveaway_data[guild_id] = {}
        self.giveaway_data[guild_id][message.id] = {
            "prize": prize,
            "duration": duration_seconds,
            "winners": winners,
            "participants": []
        }
        await self.save_giveaway_data()

        while duration_seconds > 0:
            await asyncio.sleep(1)
            duration_seconds -= 1
            time_left = discord.utils.format_dt(discord.utils.utcnow() + timedelta(seconds=duration_seconds),
                                                style='F')
            embed.set_field_at(0, name="Time Left", value=time_left)
            await message.edit(embed=embed)

        message = await ctx.channel.fetch_message(message.id)
        reactions = message.reactions
        participants = []
        for reaction in reactions:
            if str(reaction.emoji) == emoji:
                async for user in reaction.users():
                    if user != self.bot.user:
                        participants.append(user)
                break

        if len(participants) >= winners:
            winners_list = random.sample(participants, winners)
            winners_mentions = ", ".join([winner.mention for winner in winners_list])
            embed = discord.Embed(title="**Giveaway Ended**", description=f"Congratulations {winners_mentions} You won {prize}!", color=0x410142)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1216744904898646200/1221869676720685157/Giveaway-Header.png?ex=661425d0&is=6601b0d0&hm=ad44e38453a0b59783b1b087&')
        else:
            embed = discord.Embed(title="**Giveaway Ended**", description="Not enough participants to determine winners.", color=0x410142)
            embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/1216744904898646200/1221869676720685157/Giveaway-Header.png?ex=661425d0&is=6601b0d0&hm=ad44e38453a0b59783b1b087&')

        await ctx.send(embed=embed)

        # Save giveaway history
        await self.save_giveaway_history(guild_id, {
            "host": ctx.author.id,
            "prize": prize,
            "winners": [winner.id for winner in winners_list],
            "guild_id": guild_id
        })

    @_giveaway.command()
    async def reroll(self, ctx, giveaway_id: int):
        if not await self.has_admin_permissions(ctx):
            return
        if not await self.has_admin_permissions(ctx):
            return await ctx.send("You do not have enough permissions to use this command.")

        guild_id = ctx.guild.id

        if guild_id in self.giveaway_data and giveaway_id in self.giveaway_data[guild_id]:
            data = self.giveaway_data[guild_id][giveaway_id]
            participants = data["participants"]

            if len(participants) >= data["winners"]:
                winners_list = random.sample(participants, data["winners"])
                winners_mentions = ", ".join([winner.mention for winner in winners_list])
                embed = discord.Embed(title="Giveaway Rerolled", description=f"New winners for giveaway ID `{giveaway_id}`: {winners_mentions}!", color=0x410142)
            else:
                embed = discord.Embed(title="Giveaway Reroll Failed", description="Not enough participants to determine new winners.", color=0x410142)
        else:
            embed = discord.Embed(title="Invalid Giveaway ID", description="The specified giveaway ID does not exist.", color=0x410142)

        await ctx.send(embed=embed)

    @_giveaway.command()
    async def history(self, ctx):
        if not await self.has_admin_permissions(ctx):
            return await ctx.send("You do not have enough permissions to use this command.")

        guild_id = str(ctx.guild.id)

        try:
            with open(self.history_file, 'r') as file:
                history_data = json.load(file)

            if guild_id in history_data:
                last_giveaway = history_data[guild_id][-1]  # Get the last entry in the history list
                host = ctx.guild.get_member(last_giveaway['host'])
                winners = ', '.join([ctx.guild.get_member(winner).mention for winner in last_giveaway['winners']])
                embed = discord.Embed(title="**Giveaway History**", color=0x0000ff)
                embed.add_field(name="**Prize**", value=last_giveaway['prize'], inline=False)
                embed.add_field(name="**Host**", value=host.display_name, inline=False)
                embed.add_field(name="**Winners**", value=winners, inline=False)
                embed.add_field(name="**Guild ID**", value=last_giveaway['guild_id'], inline=False)
            else:
                embed = discord.Embed(title="No Giveaway History", description="There is no previous giveaway data for this server.", color=0x410142)
        except FileNotFoundError:
            embed = discord.Embed(title="No Giveaway History", description="There is no previous giveaway data for this server.", color=0x410142)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Giveaway(bot))
