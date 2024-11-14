import discord
from discord.ext import commands
from discord import Button, ButtonStyle, Interaction
import psutil
import sys
from datetime import datetime, timezone, timedelta
from discord.ui import Button , View 
from Extra.paginator import PaginatorView
import platform
import typing 
from typing import Union, Optional



class infobutton(discord.ui.View):
    def __init__(self, bot, author):
        super().__init__(timeout=180)
        self.bot = bot
        self.author = author
        self.color = 0x38024a
        self.list_supporters_button_disabled = False
        self.developer_button_disabled = False

    @discord.ui.button(label="Supporters", style=discord.ButtonStyle.gray, custom_id="list_supporters_button")
    async def list_supporters_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.list_supporters_button_disabled:
            if interaction.user.id != self.ctx.author.id:
              await interaction.response.send_message("It's not your session.", ephemeral=True)
            else:
              await interaction.response.send_message("You've already used this button. Use the command again to use it.", ephemeral=True)
            return

        self.list_supporters_button_disabled = True

        server_id = 1213550226128765019
        role_id = 1216053924402958336

        guild = self.bot.get_guild(server_id)
        if not guild:
            await interaction.response.send_message("Server not found.", ephemeral=True)
            return

        role = guild.get_role(role_id)
        if not role:
            await interaction.response.send_message("Role not found.", ephemeral=True)
            return

        supporters = [member for member in guild.members if role in member.roles]

        if not supporters:
            await interaction.response.send_message("No members found with the specified role.", ephemeral=True)
            return

        embed = discord.Embed(
            title="Supporters",
            description="\n".join(supporter.mention for supporter in supporters),
            color=self.color
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        embed.set_footer(
            text=f"Requested By {interaction.user}",
            icon_url=interaction.user.avatar.url
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


    @discord.ui.button(label="Developer", style=discord.ButtonStyle.gray, custom_id="developer_button")
    async def developer_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.developer_button_disabled:
            if interaction.user.id != self.ctx.author.id:
               await interaction.response.send_message("It's not your session.", ephemeral=True)
            else:
               await interaction.response.send_message("You've already used this button. Use the command again to use it.", ephemeral=True)
            return

        self.developer_button_disabled = True

        developers = {
            "Ray.ly": "1043194242476036107",
            "Shadow": "765865384011628574",
            "Bazzi": "1195470182831894558"
        }

        embed = discord.Embed(title="Info About Arch", color=self.color)
        
        for developer, user_id in developers.items():
            member = await interaction.guild.fetch_member(int(user_id))
            if member:
                activity = activity = member.activities[0] if member.activities else None
                activity_info = "None"
                if activity:
                    activity_type = activity.type.name.capitalize() if activity.type else "Unknown"
                    if isinstance(activity, discord.Game):
                        activity_name = activity.name
                    elif isinstance(activity, discord.Streaming):
                        activity_name = f"{activity.name} ({activity.platform})"
                    elif isinstance(activity, discord.CustomActivity):
                        activity_name = activity.name
                    else:
                        activity_name = "Unknown"
                    activity_info = f"{activity_type} - {activity_name}"
                embed.add_field(
                    name=f'**{developer}**',
                    value=f"Activity: {activity_info}\n[**{user_id}**](https://discord.com/users/{user_id})"
                )

        embed.set_author(name=f"{self.bot.user.name} Stats", icon_url=self.bot.user.display_avatar.url)
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text='Thanks For Using Arch', icon_url=self.bot.user.display_avatar.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)





class Buttons(discord.ui.View):
    def __init__(self, ctx):
        super().__init__(timeout=180)
        self.ctx = ctx
        self.color = 0x38024a
        self.list_roles_button_disabled = False
        self.list_admins_button_disabled = False

    async def interaction_check(self, interaction: discord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message("It's not your session.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="List Roles", style=discord.ButtonStyle.gray, custom_id="list_roles_button")
    async def list_roles_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.list_roles_button_disabled:
            if interaction.user.id != self.ctx.author.id:
                await interaction.response.send_message("It's not your session.", ephemeral=True)
            else:
                await interaction.response.send_message("You've already used this button. Use the command again to use it.", ephemeral=True)
            return

        self.list_roles_button_disabled = True

        roles = sorted(interaction.guild.roles, key=lambda x: x.position, reverse=True)
        if not roles:
            embed = discord.Embed(description="There are no roles in this server.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        role_mentions = "\n".join(f"{idx + 1}. {role.mention}" for idx, role in enumerate(roles))
        embed = discord.Embed(title=f"Roles in {interaction.guild.name}", description=role_mentions, color=self.color)
        embed.set_thumbnail(url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="List Admins", style=discord.ButtonStyle.gray, custom_id="list_admins_button")
    async def list_admins_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.list_admins_button_disabled:
            if interaction.user.id != self.ctx.author.id:
              await interaction.response.send_message("It's not your session.", ephemeral=True)
            else:
              await interaction.response.send_message("You've already used this button. Use the command again to use it.", ephemeral=True)
            return

        self.list_admins_button_disabled = True

        admins = [member for member in interaction.guild.members if member.guild_permissions.administrator]
        if not admins:
            embed = discord.Embed(description="There are no administrators in this server.")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        admin_mentions = "\n".join(f"{idx + 1}. {admin.mention}" for idx, admin in enumerate(admins))
        embed = discord.Embed(title=f"Admins in {interaction.guild.name}", description=admin_mentions, color=self.color)
        embed.set_thumbnail(url=interaction.guild.icon.url)

        await interaction.response.send_message(embed=embed, ephemeral=True)

class Extra(commands.Cog, name="extra"):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        self.color = 0x38024a
    
    @commands.group(name="avatar", aliases=["av"])
    async def avatar(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand. Use `avatar user` or `avatar server`.")

    from typing import Union, Optional

    @avatar.command(name="user")
    async def avatar_user(self, ctx, user: Optional[Union[discord.User, int]] = None):
        if user is None:
            user = ctx.author

        if isinstance(user, int):
            user = self.bot.get_user(user)
            if user is None:
                return await ctx.send("User not found.")

        avatar_url = user.avatar.url if user.avatar else user.default_avatar.url
        embed = discord.Embed(
            title=f"{user.name}'s Avatar",
            color=self.color
        )
        embed.set_image(url=avatar_url)

        button_label = "Download"
        view = discord.ui.View()
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label=button_label, url=avatar_url))
        
        await ctx.send(embed=embed, view=view)

    @avatar.command(name="server")
    async def avatar_server(self, ctx):
        server_avatar_url = ctx.guild.icon.url if ctx.guild.icon else ctx.guild.default_icon.url
        embed = discord.Embed(
            title="Server Icon",
            color=self.color
        )
        embed.set_image(url=server_avatar_url)
        button_label = "Download"
        view = discord.ui.View()
        view.add_item(discord.ui.Button(style=discord.ButtonStyle.link, label=button_label, url=server_avatar_url))
        await ctx.send(embed=embed, view=view)

    @commands.group(name="banner", aliases=["bn"])
    async def banner(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Invalid subcommand. Use `banner user` or `banner server`.")

    @banner.command(name="user")
    async def _user(self, ctx , member: discord.User = None):
        if member is None:
            member = ctx.author

        banner_user = await self.bot.fetch_user(member.id)
        if not banner_user.banner:
            await ctx.reply("{} does not have a banner.".format(member))
            return

        embed = discord.Embed(
            color=0x0565ff,
            description=f"[Download]({banner_user.banner.url})"
        )
        embed.set_author(
            name=f"{member}",
            icon_url=member.avatar.url if member.avatar else member.default_avatar.url
        )
        embed.set_image(url=banner_user.banner.url)
        embed.set_footer(
            text=f"Requested By {ctx.author}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        )
        view = discord.ui.View()
        button = discord.ui.Button(style=discord.ButtonStyle.link, label="Download", url=banner_user.banner.url)
        view.add_item(button)
        await ctx.reply(embed=embed, view=view)

    @banner.command(name="server")
    async def server(self, ctx):
        if not ctx.guild.banner:
            await ctx.reply("This server does not have a banner.")
            return

        embed = discord.Embed(
            color=0x0565ff,
            description=f"[Download]({ctx.guild.banner.url})"
        )
        embed.set_image(url=ctx.guild.banner.url)
        embed.set_author(
            name=ctx.guild.name,
            icon_url=ctx.guild.icon.url if ctx.guild.icon else ctx.guild.default_icon.url
        )
        embed.set_footer(
            text=f"Requested By {ctx.author}",
            icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url
        )
        view = discord.ui.View()
        button = discord.ui.Button(style=discord.ButtonStyle.link, label="Download", url=ctx.guild.banner.url)
        view.add_item(button)
        await ctx.reply(embed=embed, view=view)


   

   
    @commands.command(name="serverinfo", aliases=['si'], help="Display detailed information about the server.")
    async def serverinfo(self, ctx):
      
        total_channels = len(ctx.guild.channels)
        
        total_voice_channels = len(ctx.guild.voice_channels)
      
        locked_channels = sum(1 for channel in ctx.guild.channels if channel.overwrites_for(ctx.guild.default_role).read_messages == False)
      
        total_bots = sum(1 for member in ctx.guild.members if member.bot)
      
        total_roles = len(ctx.guild.roles)
         
        boost_level = ctx.guild.premium_subscription_count
        boost_tier = ctx.guild.premium_tier

       
        booster_role = ctx.guild.premium_subscriber_role
        booster_info = f"Count: {boost_level}\nTier: {boost_tier}\nBooster Role: {booster_role.mention if booster_role else 'None'}" if booster_role else f"Count: {boost_level}\nTier: {boost_tier}"

      
        mfa_level = "Enabled" if ctx.guild.mfa_level == discord.enums.MFALevel.require_2fa else "Disabled"
       
        widget_status = "Enabled" if ctx.guild.widget_enabled else "Disabled"

       
        explicit_content_filter_status = "Enabled" if ctx.guild.explicit_content_filter != discord.enums.ContentFilter.disabled else "Disabled"

       
        default_notifications = "All Messages" if ctx.guild.default_notifications == discord.enums.NotificationLevel.all_messages else "Only @mentions"

        
        features = ', '.join(feature.replace('_', ' ').title() for feature in ctx.guild.features) if ctx.guild.features else "None"

       
        system_channel_flags = str(ctx.guild.system_channel_flags).replace('SystemChannelFlags', '').replace('value=', '').replace('<', '').replace('>', '').strip()

      
        embed = discord.Embed(
            title=f"{ctx.guild.name}'s Information",
            color=self.color
        )
        embed.set_thumbnail(url=ctx.guild.icon.url)
      
        embed.add_field(name="Server ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="Owner", value=ctx.guild.owner.mention, inline=False)
        embed.add_field(name="Members", value=f"Total: {ctx.guild.member_count}\nBots: {total_bots}", inline=False)
       
        embed.add_field(name="Total Channels", value=total_channels, inline=False)
        embed.add_field(name="Text Channels", value=len(ctx.guild.text_channels), inline=False)
        embed.add_field(name="Voice Channels", value=total_voice_channels, inline=False)
        embed.add_field(name="Locked Channels", value=locked_channels, inline=False)
        
        embed.add_field(name="Roles", value=total_roles, inline=False)
       
        embed.add_field(name="Boost", value=booster_info, inline=False)
        
        embed.add_field(name="Created At", value=ctx.guild.created_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        
        embed.add_field(name="Verification Level", value=str(ctx.guild.verification_level), inline=False)
        embed.add_field(name="Explicit Content Filter", value=explicit_content_filter_status, inline=False)
        embed.add_field(name="Default Notification Settings", value=default_notifications, inline=False)
      
        afk_info = f"Channel: {ctx.guild.afk_channel.name if ctx.guild.afk_channel else 'None'}\nTimeout: {ctx.guild.afk_timeout} seconds"
        embed.add_field(name="AFK", value=afk_info, inline=False)
        
        embed.add_field(name="Custom Emoji Count", value=str(len(ctx.guild.emojis)), inline=False)
     
        embed.add_field(name="System Channel", value=str(ctx.guild.system_channel), inline=False)
        embed.add_field(name="System Channel Flags", value=system_channel_flags, inline=False)
        
        embed.add_field(name="MFA Level", value=mfa_level, inline=False)
    
        embed.add_field(name="Widget Enabled", value=widget_status, inline=False)
        embed.add_field(name="Widget Channel", value=str(ctx.guild.widget_channel), inline=False)
       
        embed.add_field(name="Features", value=features, inline=False)
        
       
        embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
        embed.set_image(url=ctx.guild.banner.url)
    
        view = Buttons(ctx)
        await ctx.reply(embed=embed,view=view)








    @commands.command(name='mebercount', aliases=['mc'])
    async def membercount(self, ctx):
        online_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.online)
        idle_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.idle)
        dnd_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.dnd)
        offline_members = sum(1 for member in ctx.guild.members if member.status == discord.Status.offline)

        embed = discord.Embed(
            title=f"Member Count in {ctx.guild.name}",
            color=self.color
        )
        embed.add_field(name="Total Members", value=f"{ctx.guild.member_count}", inline=False)
        embed.add_field(name="Online Members", value=f"{online_members}", inline=True)
        embed.add_field(name="Idle Members", value=f"{idle_members}", inline=True)
        embed.add_field(name="Do Not Disturb", value=f"{dnd_members}", inline=True)
        embed.add_field(name="Offline Members", value=f"{offline_members}", inline=True)
        View= Buttons(ctx)
        await ctx.send(embed=embed,view=View)
    
    
    @commands.group(name='_list',aliases=['list'])
    async def _list(self,ctx):
        if ctx.invoked_subcommand is None:
            ctx.send("The sub cmds for _list\nlist admins\nlist roles\nlist boosters")
    @_list.command(name="list_boosters", aliases=['boosters'])
    async def boosters(self, ctx):
        booster_role = ctx.guild.premium_subscriber_role
        if not booster_role:
            embed = discord.Embed(title="Error", description="Booster role not found.", color=self.color)
            await ctx.send(embed=embed)
            return

        boosters = booster_role.members
        if not boosters:
            embed = discord.Embed(title="Info", description="No boosters found.", color=discord.Color.blue())
            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_image(url='https://cdn.discordapp.com/attachments/1210268753036705882/1222035306908487811/tenor.gif?ex=661dfa91&is=660b8591&hm=94863efaefa3d2e112e6c6f0&')
            embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return
            
        paginated_boosters = [boosters[i:i + 10] for i in range(0, len(boosters), 10)]
        embeds = []

        for idx, page in enumerate(paginated_boosters, start=1):
            embed = discord.Embed(
                title=f"Boosters (Page {idx}/{len(paginated_boosters)})",
                color=0x65047d
            )

            for num, member in enumerate(page, start=(idx - 1) * 10 + 1):
                embed.add_field(name=f"#{num} User ID: {member.id}", value=f"Mention: {member.mention}", inline=False)

            embed.set_thumbnail(url=self.bot.user.avatar.url)
            embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
            embed.set_image(url='https://cdn.discordapp.com/attachments/1210268753036705882/1222035306908487811/tenor.gif?ex=661dfa91&is=660b8591&hm=e569f251e7914c736fa8f1e0c8ad0029cbb14fdd94863efaefa3d2e112e6c6f0&')
            embed.set_footer(text=f'Page {idx}/{len(paginated_boosters)} | Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)

            embeds.append(embed)

        paginator_view = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
        await ctx.send(embed=paginator_view.initial, view=paginator_view)
    
    @commands.command(name="statistics", aliases=["st", "stats"], usage="stats")
    async def stats(self, ctx):
            server_count = len(self.bot.guilds)
            total_members = sum(g.member_count for g in self.bot.guilds if g.member_count is not None)
            total_memory = psutil.virtual_memory().total >> 20
            used_memory = psutil.virtual_memory().used >> 20
            cpu_used = str(psutil.cpu_percent())

            embed = discord.Embed(
                color=self.color,
                description="[Invite](https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot) | [Support](https://discord.gg/NszXeFQTmE)"
            )

            embed.add_field(name='﹒SERVERS', value=f'```Total: {server_count} SERVERS```')
            embed.add_field(name='﹒USERS', value=f'```Total: {total_members} USERS```')
            embed.add_field(name="﹒SYSTEM", value=f"```RAM: {used_memory}/{total_memory} MB\nCPU: {cpu_used}% USED.```")
            embed.add_field(name="﹒PYTHON VERSION", value=f"```{sys.version}```")
            embed.add_field(name='﹒DISCORD.PY VERSION', value=f'```{discord.__version__}```')
            embed.add_field(name="﹒PING", value=f"```{round(self.bot.latency * 1000, 2)} MS```")

            # Creating the developer button

            # Adding the developer button to the view
            bot = self.bot
            view = infobutton(bot, ctx.author)
           

            await ctx.send(embed=embed, view=view)



    @commands.command(name='ping', help='Ping the bot.')
    async def ping(self, ctx):
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(title='<a:ping:1225124708379398246> Pong !!', description=f"<:curvedline_B:1224397348667527274>**websocket Latency**  : {latency}ms")
        await ctx.reply(embed=embed)
        
   

    @_list.command(name='list_roles', help='Displays a paginated _list of roles in the server.', aliases=['roles'])
    async def allroles(self, ctx):
        roles = ctx.guild.roles

        if not roles:
            embed = discord.Embed(
                title="No Roles",
                description="There are no roles in this server.",
                color=self.color  # Change to your desired color
            )
            await ctx.send(embed=embed)
            return

        # Paginate the roles _list
        paginated_roles = [roles[i:i + 10] for i in range(0, len(roles), 10)]
        embeds = []

        for idx, page in enumerate(paginated_roles, start=1):
            embed = discord.Embed(
                title=f"Roles in {ctx.guild.name} `(Page {idx}/{len(paginated_roles)})`",
                color=self.color  # Change to your desired color
            )

            for num, role in enumerate(page, start=(idx - 1) * 10 + 1):
                mention= role.mention
                embed.add_field(name=f"{num}. Role ID : `{role.id}`", value=f"{mention}", inline=False)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=f"Page {idx}/{len(paginated_roles)}")
            embeds.append(embed)

        # Create PaginatorView and send the paginated embeds
        paginator_view = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
        await ctx.send(embed=paginator_view.initial, view=paginator_view)

    @_list.command(name='list_admins', help='Displays a paginated _list of administrators in the server.', aliases=['admins'])
    async def administrators(self, ctx):
        admins = [member for member in ctx.guild.members if member.guild_permissions.administrator]

        if not admins:
            embed = discord.Embed(
                title="No Administrators",
                description="There are no administrators in this server.",
                color=self.color  # Change to your desired color
            )
            await ctx.send(embed=embed)
            return

        # Paginate the admins _list
        paginated_admins = [admins[i:i + 10] for i in range(0, len(admins), 10)]
        embeds = []

        for idx, page in enumerate(paginated_admins, start=1):
            embed = discord.Embed(
                title=f"Administrators in {ctx.guild.name} (Page {idx}/{len(paginated_admins)})",
                color=self.color  # Change to your desired color
            )

            for num, admin in enumerate(page, start=(idx - 1) * 10 + 1):
                embed.add_field(name=f'{num}.**User ID** : `{admin.id}`',value=f'{admin.mention}' , inline=False)
            embed.set_thumbnail(url=ctx.guild.icon.url)
            embed.set_footer(text=f"Page {idx}/{len(paginated_admins)}")
            embeds.append(embed)

        # Create PaginatorView and send the paginated embeds
        paginator_view = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
        await ctx.send(embed=paginator_view.initial, view=paginator_view)

    @commands.command(name='userinfo', help='Displays information about a user.')
    async def userinfo(self, ctx, user: discord.Member = None):
       user = user or ctx.author
  
       embed = discord.Embed(title=f"{user.name}'s Information", color=self.color)
       embed.add_field(name="User ID", value=user.id, inline=False)
       embed.add_field(name="Joined Server", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
       embed.add_field(name="Created Account", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
       embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
       await ctx.send(embed=embed)
 

    @commands.command(name="botinfo", aliases=['bi'], help="Get info about me!", with_app_command=True)
    async def botinfo(self, ctx: commands.Context):
        users = sum(g.member_count for g in self.bot.guilds if g.member_count is not None)
        channel = len(set(self.bot.get_all_channels()))
        embed = discord.Embed(
            color=self.color,
            title="About Arch",
            description=f"""\n
    **Bot's Mention:** {self.bot.user.mention}\n
    **Bot's Username:** {self.bot.user}\n
    **Total Guilds:** {len(self.bot.guilds)}\n
    **Total Users:** {users}\n
    **Total Channels:** {channel}\n
    **Total Commands: **{len(set(self.bot.walk_commands()))}\n
    **Total Shards:** {len(self.bot.shards)}\n
    **CPU usage:** {round(psutil.cpu_percent())}%\n
    **Memory usage:** {int((psutil.virtual_memory().total - psutil.virtual_memory().available) / 1024 / 1024)} MB\n
    **My Websocket Latency:** {int(self.bot.latency * 1000)} ms\n
    **Python Version:** {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n
    **Discord.py Version:** {discord.__version__}\n
    **Operating System:** {platform.system()} {platform.release()}\n
   """)
        embed.set_footer(text=f"Requested By {ctx.author}",
                        icon_url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        bot = self.bot
        ray = infobutton(bot, ctx.author)
        await ctx.send(embed=embed,view=ray)
    @commands.command()
    async def whois(self, ctx, member: discord.User = None):
        if member is None or member == "":
            member = ctx.author
        elif member not in ctx.guild.members:
            member = await self.bot.fetch_user(member.id)

        badges = ""
        if member.public_flags.hypesquad_balance:
            badges += "<:hypesquadbalance:1215686770570825768>"
        if member.public_flags.hypesquad_bravery:
            badges += "<:hypesquadbravery:1215686743626350603>"
        if member.public_flags.hypesquad_brilliance:
            badges += "<:DGH_hypesquadbrillance:1215686832902377584>"
        if member.public_flags.early_supporter:
            badges += "<:EarlySupporter:1216385290969813093>"
        if member.public_flags.active_developer:
            badges += "<:active_developer:1216385084811116634>"
        if member.public_flags.verified_bot_developer:
            badges += "<:VerifiedBotDeveloper:1216385467994472479>"
        if member.public_flags.discord_certified_moderator:
            badges += "<:DiscordCertifiedModerator:1216385670101074000>"
        if member.public_flags.staff:
            badges += "<:DiscordStaff:1216385969578836208>"
        if member.public_flags.partner:
            badges += "<:partners:1216386169311461537>"
        if badges == "" or badges is None:
            badges += "None"

        if member in ctx.guild.members:
            nickk = f"{member.nick if member.nick else 'None'}"
            joinedat = f"<t:{round(member.joined_at.timestamp())}:R>"
        else:
            nickk = "None"
            joinedat = "None"

        kp = ""
        if member in ctx.guild.members:
            if member.guild_permissions.kick_members:
                kp += " , Kick Members"
            if member.guild_permissions.ban_members:
                kp += " , Ban Members"
            if member.guild_permissions.administrator:
                kp += " , Administrator"
            if member.guild_permissions.manage_channels:
                kp += " , Manage Channels"
            if member.guild_permissions.manage_messages:
                kp += " , Manage Messages"
            if member.guild_permissions.mention_everyone:
                kp += " , Mention Everyone"
            if member.guild_permissions.manage_nicknames:
                kp += " , Manage Nicknames"
            if member.guild_permissions.manage_roles:
                kp += " , Manage Roles"
            if member.guild_permissions.manage_webhooks:
                kp += " , Manage Webhooks"
            if member.guild_permissions.manage_emojis:
                kp += " , Manage Emojis"

            if kp is None or kp == "":
                kp = "None"

        if member in ctx.guild.members:
            if member == ctx.guild.owner:
                aklm = "Server Owner"
            elif member.guild_permissions.administrator:
                aklm = "Server Admin"
            elif member.guild_permissions.ban_members or member.guild_permissions.kick_members:
                aklm = "Server Moderator"
            else:
                aklm = "Server Member"

        bannerUser = await self.bot.fetch_user(member.id)
        embed = discord.Embed(color=self.color)
        embed.timestamp = discord.utils.utcnow()
        if not bannerUser.banner:
            pass
        else:
            embed.set_image(url=bannerUser.banner)
        embed.set_author(name=f"{member.name}'s Information",
                         icon_url=member.avatar.url
                         if member.avatar else member.default_avatar.url)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.add_field(name="__General Information__",
                        value=f"""
**Name:** {member}
**ID:** {member.id}
**Nickname:** {nickk}
**Bot?:** {'<:IconTick:1213170250267492383> Yes' if member.bot else '<:crosss:1212440602659262505> No'}
**Badges:** {badges}
**Account Created:** <t:{round(member.created_at.timestamp())}:R>
**Server Joined:** {joinedat}
            """,
                        inline=False)
        if member in ctx.guild.members:
            r = (', '.join(role.mention for role in member.roles[1:][::-1])
                 if len(member.roles) > 1 else 'None.')
            embed.add_field(name="__Role Info__",
                            value=f"""
**Highest Role:** {member.top_role.mention if len(member.roles) > 1 else 'None'}
**Roles [{f'{len(member.roles) - 1}' if member.roles else '0'}]:** {r if len(r) <= 1024 else r[0:1006] + ' and more...'}
**Color:** {member.color if member.color else '000000'}
                """,
                            inline=False)
        if member in ctx.guild.members:
            embed.add_field(
                name="__Extra__",
                value=f"**Boosting:** {f'<t:{round(member.premium_since.timestamp())}:R>' if member in ctx.guild.premium_subscribers else 'None'}\n**Voice <:icons_mic:1124695914397827224>:** {'None' if not member.voice else member.voice.channel.mention}",
                inline=False)
        if member in ctx.guild.members:
            embed.add_field(name="__Key Permissions__",
                            value=", ".join([kp]),
                            inline=False)
        if member in ctx.guild.members:
            embed.add_field(name="__Acknowledgement__",
                            value=f"{aklm}",
                            inline=False)
        if member in ctx.guild.members:
            embed.set_footer(
                text=f"Requested by {ctx.author}",
                icon_url=ctx.author.avatar.url
                if ctx.author.avatar else ctx.author.default_avatar.url)
        else:
            if member not in ctx.guild.members:
                embed.set_footer(
                    text=f"{member.name} not in this this server.",
                    icon_url=ctx.author.avatar.url
                    if ctx.author.avatar else ctx.author.default_avatar.url)
        await ctx.send(embed=embed)
async def setup(bot):
   await bot.add_cog(Extra(bot))
