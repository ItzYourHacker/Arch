from discord.ext import commands
import discord
from discord.ui import Button
from typing import List
from collections import deque

class PaginatorView(discord.ui.View):
    def __init__(
        self,
        embeds: List[discord.Embed],
        bot: commands.AutoShardedBot,
        source: discord.Message,
        author
    ) -> None:
        super().__init__(timeout=120)

        self._embeds = embeds
        self._queue = deque(embeds)
        self._len = len(embeds)
        self._current_page = 1

        if self._len > 0:
            self._initial = embeds[0]
        else:
            self._initial = discord.Embed(title="No Data", description="No data to display", color=0xFF0000)

        self.bot = bot
        self._queue[0].set_footer(text=f" • Page {self._current_page}/{self._len}")
        self.author = author

    async def update_button(self, interaction: discord.Interaction) -> None:
        for i in self._queue:
            i.set_footer(text=f"{interaction.client.user.name} • Page {self._current_page}/{self._len}", icon_url=interaction.client.user.display_avatar.url)

        await interaction.message.edit(view=self)
        await interaction.response.edit_message(embed=self._queue[0], view=self)

    async def on_timeout(self):
        for i in self.children:
            i.disabled = True
        if self.message:
            await self.message.edit(view=self)

    @discord.ui.button(emoji="<:Icon_Arrow_Left:1180915135066406953>")
    async def start(self, interaction: discord.Interaction, _):
        if self.author != interaction.user:
            return await interaction.response.send_message(f"<:crosss:1212440602659262505> | Its not your interaction.", ephemeral=True)

        self._queue = deque([self._embeds[0]])
        self._current_page = 1
        await self.update_button(interaction)
        self.message = await interaction.response.edit_message(embed=self._embeds[0])

    @discord.ui.button(label="Back")
    async def previous(self, interaction: discord.Interaction, _):
        if self.author != interaction.user:
            return await interaction.response.send_message(f"<:crosss:1212440602659262505> | Its not your interaction.", ephemeral=True)

        self._queue.rotate(1)
        embed = self._queue[0]
        self._current_page -= 1
        await self.update_button(interaction)
        self.message = await interaction.response.edit_message(embed=embed)

    @discord.ui.button(emoji="<:black_cross:1220011032655691806>")
    async def stop(self, interaction: discord.Interaction, _):
        if self.author != interaction.user:
            return await interaction.response.send_message(f"<:crosss:1212440602659262505> | Its not your interaction.", ephemeral=True)

        await self.update_button(interaction)
        self.message = await interaction.message.delete()

    @discord.ui.button(label="Next")
    async def next(self, interaction: discord.Interaction, _):
        if self.author != interaction.user:
            return await interaction.response.send_message(f"<:crosss:1212440602659262505> | Its not your interaction.", ephemeral=True)

        self._queue.rotate(-1)
        embed = self._queue[0]
        self._current_page += 1
        await self.update_button(interaction)
        self.message = await interaction.response.edit_message(embed=embed)

    @discord.ui.button(emoji="<:Icon_Arrow_Right:1180915218554032251>")
    async def end(self, interaction: discord.Interaction, _):
        if self.author != interaction.user:
            return await interaction.response.send_message(f"<:crosss:1212440602659262505> | Its not your interaction.", ephemeral=True)

        self._queue = deque([self._embeds[-1]])
        self._current_page = self._len
        await self.update_button(interaction)
        self.message = await interaction.response.edit_message(embed=self._embeds[-1])


    @property
    def initial(self) -> discord.Embed:
        return self._initial
