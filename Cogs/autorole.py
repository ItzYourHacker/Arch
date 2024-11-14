import discord
from discord.ext import commands
import json
import os
role = './Database/autorole.json'
def json_load(client):
    with open(role, 'r') as f:
        pp = json.load(f)
        for guild in client.guilds:
            if str(guild.id) not in pp:
                pp[str(guild.id)] = {"humanautoroles": [], "botautoroles": []}
                with open(role, 'w') as f:
                    json.dump(pp, f, indent=4)

def reset_all(guild):
    with open(role, 'r') as f:
        pp = json.load(f)
        if guild:
            if guild:
                pp[str(guild.id)] = {"humanautoroles": [], "botautoroles": []}
                with open(role, 'w') as f:
                    json.dump(pp, f, indent=4)

def reset_human(guild):
    with open(role, 'r') as f:
        pp = json.load(f)
        if guild:
            if guild:
                pp[str(guild.id)]["humanautoroles"] = []
                with open(role, 'w') as f:
                    json.dump(pp, f, indent=4)

def reset_bot(guild):
    with open(role, 'r') as f:
        pp = json.load(f)
        if guild:
            if guild:
                pp[str(guild.id)]["botautoroles"] = []
                with open(role, 'w') as f:
                    json.dump(pp, f, indent=4)

class Autorole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x270136

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is online now")
        json_load(self.bot)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        json_load(self.bot)

    @commands.group(name="autorole", invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def autorole(self, ctx):
        prefix = ctx.prefix
        embed = discord.Embed(color=self.color,
                              title=f"`{prefix}autorole`",
                              description=
                              f"`{prefix}autorole `\nShows autorole help\n\n`{prefix}autorole humans`\nSetup autoroles for human users.\n\n`{prefix}autorole config`\nGet autorole config for the server.\n\n`{prefix}autorole reset`\nClear autorole config for the server.\n\n`{prefix}autorole bots`\nSetup autroles for bots."
                              )

        embed.set_footer(text=f"The Arch", icon_url=self.bot.user.avatar)

        await ctx.reply(embed=embed)

    @autorole.group(name="reset")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reset_all_group(self, ctx):
        if ctx.subcommand_passed is None:
            prefix = ctx.prefix
            embed = discord.Embed(
                title=f"`{prefix}autorole reset`",
                description=f"`{prefix}autorole reset bots`\nClears autorole config for the server.\n\n`{prefix}autorole reset all`\nClears autorole config for the server.\n\n`{prefix}autorole reset humans`\nClears autorole config for the server.", color=self.color)
            embed.set_footer(text="The Arch • Page 1/1", icon_url=self.bot.user.avatar)
            await ctx.reply(embed=embed)

    @reset_all_group.command(name="all")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def reset_all_cmd(self, ctx):
        if ctx.guild.me.top_role >= ctx.message.author.top_role:
            embed = discord.Embed(
                description="<:crosss:1212440602659262505> | Your top role should be above my top role.",
                color=self.color
            )
            return await ctx.reply(embed=embed)
        reset_all(ctx.guild)
        embed = discord.Embed(
            description="<:IconTick:1213170250267492383> | Successfully cleared all autoroles for this server.",
            color=self.color
        )
        await ctx.reply(embed=embed)

    @reset_all_group.command(name="humans")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reset_human_cmd(self, ctx):
        if ctx.guild.me.top_role >= ctx.message.author.top_role:
            embed = discord.Embed(
                description="<:crosss:1212440602659262505> | Your top role should be above my top role.",
                color=self.color
            )
            return await ctx.reply(embed=embed)
        reset_human(ctx.guild)
        embed = discord.Embed(
            description="<:IconTick:1213170250267492383> | Successfully cleared all human autoroles for this server.",
            color=self.color
        )
        await ctx.reply(embed=embed)

    @autorole.group(name="humans")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def humans(self, ctx):
        if ctx.subcommand_passed is None:
            client = self.bot
            embed = discord.Embed(
                title=f"`{ctx.prefix}autorole humans`",
                description=f"`{ctx.prefix}autorole humans add <role>`\nAdd a role to list of autoroles for human users.\n\n`{ctx.prefix}autorole humans remove <role>`\nRemove a role from autoroles for human users.", color=self.color
            )
            embed.set_footer(text=f"The Arch • Page 1/1", icon_url=client.user.avatar)
            await ctx.reply(embed=embed)

    @humans.command(name="add", description="Add a role in human autorole")
    @commands.has_permissions(administrator=True)
    async def humans_add(self, ctx, role: discord.Role):
        client = self.bot
        me = ctx.guild.me
        if me.top_role >= ctx.message.author.top_role:
            embed = discord.Embed(
                description="<:crosss:1212440602659262505> | Your top role should be above my top role.",
                color=self.color
            )
            return await ctx.reply(embed=embed)
        else:
            with open(role, 'r') as f:
                ff = json.load(f)
                omk = ff.get(str(ctx.guild.id))
            if str(role.id) in omk['humanautoroles']:
                embed = discord.Embed(
                    description=f"{role.mention} is already in human autoroles.",
                    color=self.color
                )
                return await ctx.reply(embed=embed)
            else:
                ff[str(ctx.guild.id)]['humanautoroles'].append(str(role.id))
                with open(role, 'w') as f:
                    json.dump(ff, f, indent=4)
                embed = discord.Embed(
                    description=f"{role.mention} has been added to human autoroles.",
                    color=self.color
                )
                await ctx.reply(embed=embed)

    @humans.command(name="remove", description="Remove a role from human autorole")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def humans_remove(self, ctx, role: discord.Role):
        client = self.bot
        me = ctx.guild.me
        if me.top_role >= ctx.message.author.top_role:
            embed = discord.Embed(
                description="<:crosss:1212440602659262505> | Your top role should be above my top role.",
                color=self.color
            )
            return await ctx.reply(embed=embed)
        else:
            with open(role, 'r') as f:
                ff = json.load(f)
                omk = ff.get(str(ctx.guild.id))
                if not str(str(role.id)) in omk['humanautoroles']:
                    embed = discord.Embed(
                        description=f"{role.mention} is not in human autoroles.",
                        color=self.color
                    )
                    return await ctx.reply(embed=embed)
                else:
                    ff[str(ctx.guild.id)]['humanautoroles'].remove(str(role.id))
                    with open(role, 'w') as f:
                        json.dump(ff, f, indent=4)

                    embed = discord.Embed(
                        description=f"{role.mention} has been removed from human autoroles.",
                        color=self.color
                    )
                    await ctx.reply(embed=embed)

    @autorole.group(name="bots")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bots(self, ctx):
        if ctx.subcommand_passed is None:
            client = self.bot
            embed = discord.Embed(
                title=f"`{ctx.prefix}autorole bots`",
                description=f"`{ctx.prefix}autorole bots add <role>`\nAdd role to list of autoroles for bot users.\n\n`{ctx.prefix}autorole bots remove <role>`\nRemove a role from autoroles for bot users.", color=self.color
            )
            embed.set_footer(text=f"The Arch • Page 1/1", icon_url=client.user.avatar)
            await ctx.reply(embed=embed)

    @bots.command(name="add", description="Add a role in bot autorole")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bots_add(self, ctx, role: discord.Role):
        client = self.bot
        me = ctx.guild.me
        if me.top_role >= ctx.message.author.top_role:
            embed = discord.Embed(
                description="<:crosss:1212440602659262505> | Your top role should be above my top role.",
                color=self.color
            )
            return await ctx.reply(embed=embed)
        else:
            with open(role, 'r') as f:
                ff = json.load(f)
            omk = ff.get(str(ctx.guild.id))
            if str(role.id) in omk['botautoroles']:
                embed = discord.Embed(
                    description=f"{role.mention} is already in bot autoroles.",
                    color=self.color
                )
                return await ctx.reply(embed=embed)
            else:
                ff[str(ctx.guild.id)]['botautoroles'].append(str(role.id))
                with open(role, 'w') as f:
                    json.dump(ff, f, indent=4)
                embed = discord.Embed(
                    description=f"{role.mention} has been added to bot autoroles.",
                    color=self.color
                )
                await ctx.reply(embed=embed)

    @bots.command(name="remove", description="Remove a role from bot autorole")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def bots_remove(self, ctx, role: discord.Role):
        client = self.bot
        me = ctx.guild.me
        if me.top_role >= ctx.message.author.top_role:
            embed = discord.Embed(
                description="<:crosss:1212440602659262505> | Your top role should be above my top role.",
                color=self.color
            )
            return await ctx.reply(embed=embed)
        else:
            with open(role, 'r') as f:
                ff = json.load(f)
            omk = ff.get(str(ctx.guild.id))
            if not str(role.id) in omk['botautoroles']:
                embed = discord.Embed(
                    description=f"{role.mention} is not in bot autoroles.",
                    color=self.color
                )
                return await ctx.reply(embed=embed)
            else:
                ff[str(ctx.guild.id)]['botautoroles'].remove(str(role.id))
                with open(role, 'w') as f:
                    json.dump(ff, f, indent=4)
                embed = discord.Embed(
                    description=f"{role.mention} has been removed from bot autoroles.",
                    color=self.color
                )
                await ctx.reply(embed=embed)

    @autorole.group(name="config")
    @commands.has_permissions(administrator=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def auto_rolshow(self, ctx):
        if ctx.subcommand_passed is None:
            client = self.bot
            with open(role, 'r') as f:
                ok = json.load(f)
            g = ok.get(str(ctx.guild.id))
            bye1 = []
            bye2 = []
            human_autoroles = g['humanautoroles']
            bot_at = g['botautoroles']
            if human_autoroles == [] and bot_at == []:
                embed = discord.Embed(
                    description=f"<:crosss:1212440602659262505> | This server don't have any autoroles setupped.",
                    color=self.color
                )
                return await ctx.reply(embed=embed)
            else:
                if human_autoroles == []:
                    bye1.append(f"Not Set")
                else:
                    for idkft in human_autoroles:
                        bye1.append(f"<@&{idkft}>")
                if bot_at == []:
                    bye2.append(f"Not Set")
                else:
                    for item in bot_at:
                        bye2.append(f"<@&{item}>")
                embed = discord.Embed(title=f"**{ctx.guild.name} Autorole Settings <:icons_human:1214804075368157194>**",
                                      color=self.color)
                embed.add_field(name="__**Humans**__", value="\n".join(bye1))
                embed.add_field(name="__**Bots**__", value="\n".join(bye2))

            await ctx.reply(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)

        # Check if autoroles are configured for the guild
        with open(role, 'r') as f:
            autorole_config = json.load(f).get(guild_id)

        if autorole_config:
            # Assign human autoroles
            human_roles = [member.guild.get_role(int(role_id)) for role_id in autorole_config['humanautoroles']]
            await member.add_roles(*[role for role in human_roles if role])

            # Assign bot autoroles (if the member is a bot)
            if member.bot:
                bot_roles = [member.guild.get_role(int(role_id)) for role_id in autorole_config['botautoroles']]
                await member.add_roles(*[role for role in bot_roles if role])

async def setup(bot):
    await bot.add_cog(Autorole(bot))
