import discord
import asyncio
from discord.ext import commands
from discord import app_commands, SelectOption, Button
from discord import ButtonStyle
link1 = "https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot"
link = "https://discord.com/invite/archdev"

giveaway = "<:icon_GiveawayIcon:1214584516849696788>"
Extra = "<:extra:1213546253649186926>"
autoresp = "<:icon_12:1214562796755484744>"
moderation = "<:moderation:1212415056772595714>"
utility = "<:utility:1214563086585954344>"
leaderboards = "<:icons_loading:1214569603292725330>"
Custom_roles = "<:ruby_antinuke:1212414349738647582>"
info = "<:error:1212814863240400946>"
antinuke = "<:automod:1212414534963433482>"
autorole ="<:autoroles:1217137198738968677>"
music = "<:icons_Music:1213177796336164944>"
class MenuView(discord.ui.View):
    def __init__(self, author, timeout=60):
        super().__init__(timeout=timeout)
        self.author = author
        self.color = 0x49015e
    @discord.ui.select(placeholder="Hey !! I'm Arch  ", options=[
        SelectOption(label="Moderation", value="moderation"),
        SelectOption(label="Autoresponder", value="autoresponder"),
        SelectOption(label="Music", value="music"),
        SelectOption(label="Utility", value="utility"),
        SelectOption(label="Autorole", value="Autorole"),
        SelectOption(label="Trigger roles", value="Trigger roles"),
        SelectOption(label="Info", value="info"),
        SelectOption(label="Giveaway", value="giveaway")
    ])
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        try:
            if interaction.user.id != self.author.id:
                await interaction.response.send_message("This is not your interaction.", ephemeral=True)
                return
            selected_values = select.values
            
            if selected_values and "moderation" in selected_values:
                embed = discord.Embed(color=self.color, description="```Kick, Ban, Unban, Mute, Unmute, Lock, Lockall, Unlockall, Hideall, Unhideall Addrole, Delrole, Role bots, Role all, Role, Role humans, Role staus, Role cancel,  Roleremove, Rrole all, Rrole bots, Rrole humans , Rrole status, Rrole cancle, Roleicon, Purge, Purge user, Purge startswith, Purge endswith, Purge invites, Purge bots, Snipe, Clone, Nuke, Addemoji, Delemoji, Addsticker ,Delsticker```")
                embed.set_author(name="Moderation Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "autoresponder" in selected_values:
                embed = discord.Embed(color=self.color, description="```Autoresponder, Autoresponder Create, Autoresponder Delete, Autoresponder config, Autoreponder edit```")
                embed.set_author(name="Autoresponder Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "music" in selected_values:
                embed = discord.Embed(color=self.color, description="```Play, Stop, Skip, Previous, Queue, Clearqueue, Removequeue, Volume, Join, Move, Leave, Nowplaying, Seek, End, Shuffle, Autoplay, Skipto, Loop, Grab,```\nFilters\n``` Nightcore```")
                embed.set_author(name="Music Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "utility" in selected_values:
                embed = discord.Embed(color=self.color, description="```Avatar user, Banner user, Banner server, Membercount, Userinfo, Whois, Afk, List Boosters, List Roles, List Admins, Serverinfo```")
                embed.set_author(name="Utility Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "Autorole" in selected_values:
                embed = discord.Embed(color=self.color, description="```Autorole, Autorole config, Autorole humans add, Autorole humans remove, Autoroles bots add, Autoroles bots remove, Autorole reset, Autorole reset all, Autorole reset humans, Autorole reset bots```")
                embed.set_author(name="Autorole Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "trigger roles" in selected_values:
                embed = discord.Embed(color=self.color, description="```Setup, Setup reqrole, Remove reqrole, Setup config, Setup role, Remove trigger, Clear triggers, <trigger> <member>```")
                embed.set_author(name="Trigger Roles Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "info" in selected_values:
                embed = discord.Embed(color=self.color, description="```Ping, Uptime, Invite, Botinfo, Stats```")
                embed.set_author(name="Info Commands")
                await interaction.response.edit_message(embed=embed, view=self)
            elif selected_values and "giveaway" in selected_values:
                embed = discord.Embed(color=self.color, description="```Giveaway, Giveaway start, Giveaway reroll, Giveaway history```")
                embed.set_author(name="Giveaway Commands")
                await interaction.response.edit_message(embed=embed, view=self)

            select.placeholder = None
        except Exception as e:
            print(f"An error occurred: {e}")
            raise


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.remove_command("help")
        self.color = 0x49015e

    @commands.command(aliases=['h'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        view = MenuView(ctx.author)
        embed = discord.Embed(color = 0x49015e,
                              description=f'**My prefix is `$`\nTotal Commands - {len(set(self.bot.walk_commands()))}\n[The Arch]({link1}) | [Support]({link})\nThanks for using Arch\n```- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```**')
        embed.add_field(
            name="__**Modules**__",
            value=f"{autoresp} : Autoresponder\n{music} : Music\n{autorole} : Autorole\n{utility} : Utility\n{Custom_roles} : Trigger roles\n{info} : Info\n{moderation} : Moderation\n{giveaway} : Giveaway")
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(text="Powered By The Arch") 
        button1 = discord.ui.Button(style=discord.ButtonStyle.link, label="The Arch", url=link1)
        button2 = discord.ui.Button(style=discord.ButtonStyle.link, label="Support", url=link)

        view.add_item(button1)
        view.add_item(button2)

        message = await ctx.reply(embed=embed, view=view)
        try:
            await asyncio.sleep(view.timeout)
        except asyncio.CancelledError:
            pass
        else:
            for child in view.children:
                child.disabled = True
            await message.edit(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(Help(bot))