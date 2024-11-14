import discord
from discord.ext import commands
import os
import json
from Extra.paginator import PaginatorView


config_file = './Database/custom_roles.json'

with open('./Database/info.json', 'r') as f:
  Data = json.load(f)

ray = Data['OWNER_IDS']


class RoleCog(commands.Cog, name="Utility"):

  def __init__(self, bot):
    self.bot = bot
    self.color= 0x38024a
  @commands.group(name='setup', aliases=['set'])
  async def _setup(self, ctx: commands.Context):
      print("Setup command invoked")
      if ctx.subcommand_passed is None:
          embed = discord.Embed(
              title="Trigger roles Command Help",
              description="Here are the available subcommands for the Trigger roles command:**```- [] = optional argument\n- <> = required argument\n- Do NOT Type These When Using Commands !```**",
              color=self.color
          )
          embed.add_field(name="`$Setup reqrole <roleId>`", value="Setup the required role ", inline=False)
          embed.add_field(name="`$Remove reqrole `", value="To remove the required role", inline=False)
          embed.add_field(name="`$Setup config`", value="To check the `Trigger and roles `", inline=False)
          embed.add_field(name="`$Setup role <trigger> <roleId>`", value="To create a trigger for role", inline=False)
          embed.add_field(name="`$Remove Trigger <trigger name>`", value="To remove a trigger", inline=False)
          embed.add_field(name="`$clear triggers`", value="Clear all triggers ", inline=False)
          embed.add_field(name="`<Trigger> <Member.mention>`", value="to add and remove role using trigger  .", inline=False)
          
          embed.set_thumbnail(url=self.bot.user.avatar.url)
          embed.set_footer(
              text=f"Requested By {ctx.author}",
              icon_url=ctx.author.avatar.url)
          await ctx.send(embed=embed)


  @commands.group(name="remove", invoke_without_command=False,aliases=["re"])
  async def _remove(self, ctx):
      # Provide help or default behavior for the remove command group
      pass
  async def cog_check(self, ctx):
        return (ctx.author.guild_permissions.administrator 
                or ctx.author.id == ctx.guild.owner_id 
                or ctx.author.id in ray)

  async def get_role(self, guild, role_input):
    try:
      role_id = int(role_input)
      role = guild.get_role(role_id)
      return role
    except ValueError:
      role = discord.utils.get(guild.roles, name=role_input)
      return role
  async def has_required_perms(self, ctx):
    try:
        with open(config_file, "r") as f:
            custom_roles = json.load(f)
    except json.JSONDecodeError as e:
        # Handle JSON decoding error
        print(f"Error loading JSON: {e}")
        return False

    server_id = str(ctx.guild.id)
    required_role_id = custom_roles.get(server_id, {}).get("rrole")

    return (
        ctx.author == ctx.guild.owner
        or ctx.author.guild_permissions.administrator
        or (required_role_id and any(role.id == required_role_id for role in ctx.author.roles))
    )
  @_setup.command()
  async def reqrole(self, ctx,
                                required_role: commands.RoleConverter):
    if await self.has_required_perms(ctx):
      server_id = str(ctx.guild.id)
      with open(config_file, 'r') as file:
        custom_roles = json.load(file)

      if server_id in custom_roles and 'rrole' in custom_roles[server_id]:
        embed = discord.Embed(
            title="Error",
            description=
            "<:crosss:1212440602659262505> | Only one required role can be set.",
            color=self.color)
        await ctx.send(embed=embed)
        return

      custom_roles.setdefault(server_id, {})['rrole'] = required_role.id

      with open(config_file, 'w') as file:
        json.dump(custom_roles, file, indent=2)

      embed = discord.Embed(
          title="Success",
          description=
          f"Required role set to {required_role.mention} with trigger `reqrole`.",
          color=self.color)
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
          title="Error",
          description="<:crosss:1212440602659262505> | You don't have enough permissions to use this command.",
          color=self.color)
      await ctx.send(embed=embed)

  @_remove.command(name='Remove reqrole',aliases=['reqrole'])
  async def bbbbbbbb(self, ctx):
    if await self.has_required_perms(ctx):
      server_id = str(ctx.guild.id)
      with open(config_file, 'r') as file:
        custom_roles = json.load(file)

      if server_id not in custom_roles or 'rrole' not in custom_roles[
          server_id]:
        embed = discord.Embed(
            title="Error",
            description="<:crosss:1212440602659262505> | No required role set for this server.",
            color=self.color)
        await ctx.send(embed=embed)
        return

      del custom_roles[server_id]['rrole']

      with open(config_file, 'w') as file:
        json.dump(custom_roles, file, indent=2)

      embed = discord.Embed(title="Success",
                            description="<:IconTick:1213170250267492383> | Required role removed.",
                            color=self.color)
      await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
          title="Error",
          description="<:crosss:1212440602659262505> | You don't have enough permissions to use this command.",
          color=self.color)
      await ctx.send(embed=embed)

  @_setup.command()
  async def role(self, ctx, trigger, *, role_input):
    print("Trigger:", trigger)
    print("Role Input:", role_input)
    if await self.has_required_perms(ctx):
      server_id = str(ctx.guild.id)
      print("Reading JSON file...")
      with open(config_file, "r") as f:
          custom_roles = json.load(f)
      print("Custom Roles:", custom_roles)
 
      if server_id in custom_roles and trigger in custom_roles[server_id]:
        embed = discord.Embed(
            title="Error",
            description=
            f"<:crosss:1212440602659262505> | Trigger '`{trigger}`' already exists. Use !setup trigger to update the existing trigger.",
            color=self.color)
        await ctx.send(embed=embed)
        return

      role = await self.get_role(ctx.guild, role_input)

      if role:
        if server_id not in custom_roles or len(custom_roles[server_id]) < 20:
          custom_roles.setdefault(server_id, {})[trigger] = role.id

          with open(config_file, 'w') as file:
            json.dump(custom_roles, file, indent=2)

          embed = discord.Embed(
              title="Success",
              description=f"<:IconTick:1213170250267492383> | Custom role {role.mention} set for trigger `{trigger}`.",
              color=self.color)
          await ctx.send(embed=embed)
        else:
          embed = discord.Embed(
              title="Error",
              description="**Maximum custom roles reached for this server.**",
              color=self.color)
          await ctx.send(embed=embed)
      else:
        embed = discord.Embed(
            title="Error",
            description=f"<:crosss:1212440602659262505> | Role not found for input: {role_input}.",
            color=self.color)
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
          title="Error",
          description="<:crosss:1212440602659262505> | You don't have enough permissions to use this command.",
          color=self.color)
      await ctx.send(embed=embed)

  @_remove.command()
  async def trigger(self, ctx, trigger):
    if await self.has_required_perms(ctx):
      server_id = str(ctx.guild.id)
      with open(config_file, 'r') as file:
        custom_roles = json.load(file)

      if server_id in custom_roles and trigger in custom_roles[server_id]:
        del custom_roles[server_id][trigger]

        with open(config_file, 'w') as file:
          json.dump(custom_roles, file, indent=2)

        embed = discord.Embed(
            title="Success",
            description=f"<:IconTick:1213170250267492383> | Custom role trigger `{trigger}` removed.",
            color=self.color)
        await ctx.send(embed=embed)
      else:
        embed = discord.Embed(
            title="Error",
            description=f"<:crosss:1212440602659262505> | No custom role found for trigger `{trigger}`.",
            color=self.color)
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
          title="Error",
          description="<:crosss:1212440602659262505> | You don't have enough permissions to use this command.",
          color=self.color)
      await ctx.send(embed=embed)

  @_setup.command()
  async def config(self, ctx):
    if ctx.author == ctx.guild.owner or ctx.author.guild_permissions.administrator:
      server_id = str(ctx.guild.id)
      with open(config_file, 'r') as file:
        custom_roles = json.load(file)

      if server_id in custom_roles:
        embed_pages = []
        roles = custom_roles[server_id].items()
        num_roles = len(roles)
        num_pages = (num_roles + 9) // 10
        for i in range(num_pages):
          embed = discord.Embed(
              title=f"**Configured Triggers and Roles** `(Page {i+1}/{num_pages})`",
              color=self.color)

          embed.set_thumbnail(url=self.bot.user.avatar.url)
          for j in range(10):
            index = i * 10 + j
            if index < num_roles:
              trigger, role_id = list(roles)[index]
              role = ctx.guild.get_role(role_id)
              if role:
                embed.add_field(name=f"`#{j+1}`. **Trigger**: `{trigger}`",
                                value=f"**Role**: {role.mention}",
                                inline=False)
              else:
                embed.add_field(name=f"`#{j+1}`. **Trigger**: `{trigger}`",
                                value="Role not found",
                                inline=False)

          embed_pages.append(embed)

        paginator_view = PaginatorView(embeds=embed_pages,
                                       bot=self.bot,
                                       source=ctx.message,
                                       author=ctx.author)

        message = await ctx.send(embed=embed_pages[0], view=paginator_view)

        paginator_view.message = message
      else:
        embed = discord.Embed(
            title="Error",
            description="<:crosss:1212440602659262505> | No custom roles configured for this server.",
            color=self.color)
        await ctx.send(embed=embed)
    else:
      embed = discord.Embed(
          title="Error",
          description="<:crosss:1212440602659262505> | You don't have enough permissions to use this command.",
          color=self.color)
      await ctx.send(embed=embed)
  @commands.Cog.listener()
  async def on_message(self, message):
        if message.author.bot or message.reference:
            # Ignore messages from bots and messages that are replies
            return

        with open(config_file, "r") as f:
            custom_roles = json.load(f)

        for trigger, role_id in custom_roles.get(str(message.guild.id), {}).items():
            if message.content.lower().startswith(trigger.lower()):

                role = message.guild.get_role(role_id)

                if role:
                    mentioned_users = message.mentions
                    if mentioned_users:
                        for user in mentioned_users:
                            if await self.has_required_perms(message):
                                if role in user.roles:
                                    await user.remove_roles(role)
                                    embed = discord.Embed(
                                        title="Role Removed",
                                        description=f"<:IconTick:1213170250267492383> | Role {role.mention} removed from {user.mention}.",
                                        color=self.color
                                    )
                                    await message.channel.send(embed=embed)
                                else:
                                    await user.add_roles(role)
                                    embed = discord.Embed(
                                        title="Role Added",
                                        description=f"<:IconTick:1213170250267492383> | Role {role.mention} added to {user.mention}.",
                                        color=self.color
                                    )
                                    await message.channel.send(embed=embed)
                            else:
                                embed = discord.Embed(
                                    title="Permission Error",
                                    description="**Bot doesn't have enough permissions to manage roles or you don't have the required role.**",
                                    color=self.color
                                )
                                await message.channel.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            title="Mention Required",
                            description="<:crosss:1212440602659262505> | Please mention a user to assign or remove the role.",
                            color=self.color
                        )
                        await message.channel.send(embed=embed)
                else:
                    embed = discord.Embed(
                        title="Role Not Found",
                        description="**The configured role does not exist.**",
                        color=self.color
                    )
                    await message.channel.send(embed=embed)
                break
  @commands.group(name="clear", aliases=["reset"])
  async def _clear(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            # If no subcommand is provided, send help message or default behavior
            await ctx.send_help(ctx.command)

  @_clear.command(name="triggers", aliases=["trigger"])
  async def clear_triggers(self, ctx):
        if await self.has_required_perms(ctx):
            server_id = str(ctx.guild.id)
            with open(config_file, 'r') as file:
                custom_roles = json.load(file)

            if server_id in custom_roles:
                custom_roles[server_id] = {}
                with open(config_file, 'w') as file:
                    json.dump(custom_roles, file, indent=2)

                embed = discord.Embed(
                    title="Success",
                    description="<:IconTick:1213170250267492383> | All triggers cleared for this server.",
                    color=self.color
                )
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title="Error",
                    description="<:crosss:1212440602659262505> | No custom roles configured for this server.",
                    color=self.color
                )
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description="<:crosss:1212440602659262505> | You don't have enough permissions to use this command.",
                color=self.color
            )
            await ctx.send(embed=embed)
async def setup(bot):
  await bot.add_cog(RoleCog(bot))
