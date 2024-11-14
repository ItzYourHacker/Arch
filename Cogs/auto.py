import discord
from discord.ext import commands
import json
from Extra.paginator import PaginatorView


auto='./Database/autoresponder.json'

class ray1(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(case_insensitive=True)  
    async def ar(self, ctx: commands.Context):
        if ctx.invoked_subcommand is None:
            await ctx.reply_help(ctx.command)
            ctx.command.reset_cooldown(ctx)

    @ar.command(name="create")
    @commands.has_permissions(administrator=True)
    async def _create(self, ctx, name, *, message):
        with open(auto, "r") as f:
            autoresponse = json.load(f)

        autoresponse.setdefault(str(ctx.guild.id), {})

        numbers = []
        if str(ctx.guild.id) in autoresponse:
            for autoresponsecount in autoresponse[str(ctx.guild.id)]:
                numbers.append(autoresponsecount)
            if len(numbers) >= 20:
                hacker6 = discord.Embed(
                    title="Arch",
                    description=f"<:crosss:1212440602659262505>  You can't add more than 20 autoresponses in {ctx.guild.name}",
                    color=0x00FFCA)
                hacker6.set_author(name=f"{ctx.author}",
                                   icon_url=f"{ctx.author.avatar}")
                
                return await ctx.reply(embed=hacker6)
        autoresponse[str(ctx.guild.id)][name] = message
        with open(auto, "w") as f:
            json.dump(autoresponse, f, indent=4)
        embed = discord.Embed(
                title=f"<:IconTick:1213170250267492383> | Autoresponder `{name}` created successfully.",
                
                color=0x270136 
            )
        
        embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
        await ctx.reply(embed=embed)
        

    @ar.command(name="delete")
    @commands.has_permissions(administrator=True)
    async def _delete(self, ctx, name):
        with open(auto, "r") as f:
            autoresponse = json.load(f)

        if str(ctx.guild.id) in autoresponse and name in autoresponse[str(ctx.guild.id)]:
            del autoresponse[str(ctx.guild.id)][name]
            with open(auto, "w") as f:
                json.dump(autoresponse, f, indent=4)
            embed = discord.Embed(
                title=f"<:IconTick:1213170250267492383> | Autoresponder `{name}` deleted successfully.",
                
                color=0x270136 
            )
            
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
            
        else:
            embed = discord.Embed(
                title=f"<:error:1212814863240400946> | No autoresponder found with the name `{name}`.",
                
                color=0x270136 
            )
            
            embed.set_footer(
                text=f"Requested By {ctx.author}",
                icon_url=ctx.author.avatar.url)
            await ctx.reply(embed=embed)
    @ar.command(name="config")
    async def _config(self, ctx):
        with open(auto, "r") as f:
            autoresponse = json.load(f)

        autoresponders = autoresponse.get(str(ctx.guild.id), {})
        if autoresponders:
            paginated_autoresponders = [list(autoresponders.items())[i:i + 10] for i in range(0, len(autoresponders.items()), 10)]
            embeds = []

            for page_num, page_autoresponders in enumerate(paginated_autoresponders, start=1):
                autoresponders_list = '\n'.join([f"<:curvedline_B:1224397348667527274> **`.{idx + 1}` Trigger  :  {key}**\n**```Value  : {value}```**" for idx, (key, value) in enumerate(page_autoresponders, start=(page_num - 1) * 10)])
                embed = discord.Embed(
                    title=f"**<:icon_12:1214562796755484744> | Autoresponders for {ctx.guild.name}**",
                    description=autoresponders_list,
                    color=0x270136
                )
                embed.set_thumbnail(url=ctx.guild.icon.url)
                embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar.url)
                embed.set_image(url='https://cdn.discordapp.com/attachments/1210268753036705882/1222035306908487811/tenor.gif?ex=661dfa91&is=660b8591&hm=94863efaefa3d2e112e6c6f0&')
                embed.set_footer(text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar.url)
                embeds.append(embed)

            paginator_view = PaginatorView(embeds, self.bot, ctx.message, ctx.author)
            await ctx.send(embed=paginator_view.initial, view=paginator_view)
        else:
            embed4 = discord.Embed(
                title="<:error:1212814863240400946> | No autoresponders found for this server",
                color=0x270136
            )
            await ctx.reply(embed=embed4)

    @ar.command(name="get")
    async def _get(self, ctx, name):
        with open(auto, "r") as f:
            autoresponse = json.load(f)

        autoresponder = autoresponse.get(str(ctx.guild.id), {}).get(name)
        if autoresponder:
            embed4 = discord.Embed(
                title=f"The response for Trigger : {name} is",
                description=f"`{autoresponder}`",
                color=0x270136 
            )
            await ctx.reply(embed=embed4)
        else:
            embed = discord.Embed(
                title=f"<:error:1212814863240400946> | No autoresponder found with the name `{name}`.",
                color=0x270136   
            )
            await ctx.reply(embed=embed)

    @ar.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def _clear(self, ctx):
        with open(auto, "r") as f:
            autoresponse = json.load(f)

        autoresponse[str(ctx.guild.id)] = {}
        with open(auto, "w") as f:
            json.dump(autoresponse, f, indent=4)
        embed2 = discord.Embed(
            title="<:IconTick:1213170250267492383> | All autoresponders cleared successfully.",  
            color=0x270136 
        )
        await ctx.reply(embed=embed2)

    @ar.error
    async def ar_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed3 = discord.Embed(
                title="<:error:1212814863240400946> | You don't have permission to use this command.",
                color=0x270136 
            )
            await ctx.reply(embed=embed3)

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.reply("<:error:1212814863240400946> | Please provide a name and a message for the autoresponder.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.content:
            return

        with open(auto, "r") as f:
            autoresponse = json.load(f)

        for trigger, response in autoresponse.get(str(message.guild.id), {}).items():
            if message.content.lower().startswith(trigger.lower()) and message.author != self.bot.user:
                await message.channel.send(response)
                break

async def setup(bot):
    await bot.add_cog(ray1(bot))
