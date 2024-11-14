import discord
from discord.ext import commands
from discord.ui import View, Button

link1 = "https://discord.com/oauth2/authorize?client_id=1213860294301061122&permissions=8&scope=bot"
link2 = "https://discord.com/invite/tWMWQhPcdb"

class ButtonView(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(style=discord.ButtonStyle.link, label="The Arch", url=link1))
        self.add_item(Button(style=discord.ButtonStyle.link, label="Support", url=link2))

class MentionEventCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Check if the bot is mentioned in the message
        if self.bot.user in message.mentions:
            # Check if the message only contains a mention of the bot
            if len(message.content.strip()) == len(f'<@{self.bot.user.id}>'):
                ctx = await self.bot.get_context(message)
                embed = discord.Embed(
                    title="Hey! I'm Arch",
                    description=f'**My prefix is `$`\nTotal Commands - {len(set(self.bot.walk_commands()))}\n[The Arch]({link1}) | [Support]({link2})\nThanks for using Arch**',
                    color=0x38024a
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.set_footer(text="Powered By The Arch")

                # Create and send message with embed and attached view
                await ctx.send(embed=embed, view=ButtonView())

# Add this cog to your bot
async def setup(bot):
    await bot.add_cog(MentionEventCog(bot))
