import discord
from discord.ext import commands
import aiohttp

class error(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.color = 0x38024a
    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
            em = discord.Embed(title=f"Command used in {ctx.guild.name}", description=f"Command name: `{ctx.command.qualified_name}`\nAuthor Name: {str(ctx.author)}\nGuild Id: {ctx.guild.id}\nCommand executed: `{ctx.message.content}`\nChannel name: {ctx.channel.name}\nChannel Id: {ctx.channel.id}\nJump Url: [Jump to]({ctx.message.jump_url})\nCommand runned without error: True", timestamp=ctx.message.created_at, color=self.color)
            em.set_thumbnail(url=ctx.author.display_avatar.url)
            if ctx.author.id in [1043194242476036107]:
                return
            else:
                webhook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1217136962205515798/Mxbr6ZoM3lt6pEv2my-a-rpXDSGN6YQhSlAtAbi0Zwx6z6G7Yj_nH-YIQUsFON8rt3Gr")
                webhook.send(embed=em, username=f"{str(self.bot.user)} | Command Logs", avatar_url=self.bot.user.avatar.url)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
            
            webhook = discord.SyncWebhook.from_url("https://discord.com/api/webhooks/1217136962205515798/Mxbr6ZoM3lt6pEv2my-a-rpXDSGN6YQhSlAtAbi0Zwx6z6G7Yj_nH-YIQUsFON8rt3Gr")
            try:
                emb = discord.Embed(title=f"Command used in {ctx.guild.name}", description=f"Command name: `{ctx.command.qualified_name}`\nAuthor Name: {str(ctx.author)}\nGuild Id: {ctx.guild.id}\nCommand executed: `{ctx.message.content}`\nChannel name: {ctx.channel.name}\nChannel Id: {ctx.channel.id}\nJump Url: [Jump to]({ctx.message.jump_url})\nCommand runned without error: False", timestamp=ctx.message.created_at, color=self.color)
            except:
                return
            emb.set_thumbnail(url=ctx.author.display_avatar.url)
            if isinstance(error, commands.BotMissingPermissions):
                permissions = ", ".join([f"{permission.capitalize()}" for permission in error.missing_permissions]).replace("_", " ")
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  Unfortunately I am missing **`{permissions}`** permissions to run the command `{ctx.command}`", color=self.color)
                try:
                    await ctx.send(embed=em, delete_after=7)
                except:
                    try:
                        await ctx.author.send(content=f'<:crosss:1212440602659262505>  Unfortunately I am missing **`{permissions}`** permissions to run the command `{ctx.command}` in [{ctx.channel.name}]({ctx.channel.jump_url})')
                    except:
                        pass
                emb.add_field(name="Error:", value=f"Bot Missing {permissions} permissions to run the command", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.MissingPermissions):
                permissions = ", ".join([f"{permission.capitalize()}" for permission in error.missing_permissions]).replace("_", " ")
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You lack `{permissions}` permissions to run the command `{ctx.command}`.", color=self.color)
                await ctx.send(embed=em, delete_after=7)
                emb.add_field(name="Error:", value=f"User Missing {permissions} permissions to run the command", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.MissingRole):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You need `{error.missing_role}` role to use this command.", color=self.color)
                await ctx.send(embed=em, delete_after=5)
                emb.add_field(name="Error:", value=f"Missing role", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.CommandOnCooldown):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  This command is on cooldown. Please retry after `{round(error.retry_after, 1)} Seconds` .", color=self.color)
                await ctx.send(embed=em, delete_after=7)
                emb.add_field(name="Error:", value=f"Command On Cooldown", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.MissingRequiredArgument):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  You missed the `{error.param.name}` argument.\nDo it like: `{ctx.prefix}{ctx.command.qualified_name} {ctx.command.signature}`", color=self.color)
                await ctx.send(embed=em, delete_after=7)
                emb.add_field(name="Error:", value=f"Argument missing", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.EmojiNotFound):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Emoji Cannot be found", color=self.color)
                await ctx.send(embed=em, delete_after=3)
                emb.add_field(name="Error:", value=f"Emoji not found", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.RoleNotFound):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Role Cannot be found", color=self.color)
                await ctx.send(embed=em, delete_after=3)
                emb.add_field(name="Error:", value=f"Role not found", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.GuildNotFound):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Guild Cannot be found", color=self.color)
                await ctx.send(embed=em, delete_after=3)
                emb.add_field(name="Error:", value=f"Guild not found", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.UserNotFound):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  The User Cannot be found", color=self.color)
                await ctx.send(embed=em, delete_after=3)
                emb.add_field(name="Error:", value=f"User not found", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.MemberNotFound):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Member Cannot be found", color=self.color)
                await ctx.send(embed=em, delete_after=3)
                emb.add_field(name="Error:", value=f"Member not found", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
            if isinstance(error, commands.NSFWChannelRequired):
                em = discord.Embed(description=f"<:crosss:1212440602659262505>  The Channel is required to be NSFW to execute this command", color=self.color)
                await ctx.send(embed=em, delete_after=8)
                emb.add_field(name="Error:", value=f"NSFW Channel disabled", inline=False)
                webhook.send(embed=emb, username=f"{str(self.bot.user)} | Error Command Logs", avatar_url=self.bot.user.avatar.url)
                return
async def setup(bot):
    await bot.add_cog(error(bot))
    
    
