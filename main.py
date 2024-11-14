import discord
from discord.ext import commands, tasks
import asyncio
import colorama
from colorama import Fore
from itertools import cycle
import json
import datetime
import os
from discord.ui import View, Button 
import wavelink
import time
from Extra.np import get_prefix
colorama.init(autoreset=True)

status = cycle(['The Arch | $help ', 'Ray <3', 'Shadow <3', 'Bazzi <3'])

with open('Database/info.json', 'r') as f:
    Data = json.load(f)

ray = Data['OWNER_IDS']
class Context(commands.Context):
    async def send(self, content: str = None, *args, **kwargs) -> discord.Message:
        return await super().send(content, *args, **kwargs)

intents = discord.Intents.all()

class Bot(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            intents=intents,
            shards=2,
            shard_count=2,
            help_command=None,
            case_insensitive=True,
            strip_after_prefix=True,
            status=discord.Status.dnd,
            activity=discord.Activity(type=discord.ActivityType.listening, name=next(status)),
            
        )

    async def setup_hook(self):
        self.launch_time = datetime.datetime.now(datetime.timezone.utc)

        extensions = [
            "jishaku",
            "Cogs.afk",
            "Cogs.role",
            "Cogs.extra",
            "Cogs.owner",
            "Cogs.giveaway",
            "Cogs.help",
            "Cogs.moderation",
            "Cogs.auto",
            "Cogs.mention",
            "Cogs.autorole",
            "Extra.event",
            "Extra.error_handler",
            "Cogs.emojisticker",
            "Cogs.music",
            "Cogs.message"
        ]
        for extension in extensions:
          try:
            await self.load_extension(extension)
            print(f"Loaded extension: {extension}")
          except Exception as e:
            print(f"Failed to load extension {extension}. Reason: {e}")
    
        print("connecting wavelink..")
        nodes = [wavelink.Node(uri='http://lavalink.vaproh.cloud:2333', password='Doom129', inactive_player_timeout= 10)] # decalring nodes variable
        time.sleep(0.1)
        print("connecting wavelink.")
        try:
            
            await wavelink.Pool.connect(nodes=nodes, client=self, cache_capacity=100) # connecting..
            time.sleep(0.1)
            print("Wavelink connected successfully!")
        except:
            print("cant connect")

    @tasks.loop(seconds=2)
    async def status_task(self):
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=next(status)))

    async def get_context(self, message, *, cls=None):
        return await super().get_context(message, cls=cls or Context)

    async def on_ready(self):
       
        self.status_task.start()
        ray = Fore.RED
        os.system("cls")
        print(Fore.RED + r"""
-----------------------------------------------------
| ░▒▓██████▓▒░░▒▓███████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ |
|░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ |
|░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░ |
|░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ |
|░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░ |
|░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░░▒▓██████▓▒░░▒▓█▓▒░░▒▓█▓▒░ |
 ------------------------------------------------------  """)
        print(f"{ray}Logged In As {self.user}\nID - {self.user.id}")
        print(f"{ray} Made by ray <3")
        print(f"{ray}logged In as {self.user.name}")
        print(f"{ray}Total servers ~ {len(self.guilds)}")
        print(f"{ray}Total Users ~ {len(self.users)}")

    async def on_message_edit(self, before, after):
        ctx: Context = await self.get_context(after, cls=Context)
        if before.content != after.content:
            if after.guild is None or after.author.bot:
                return
            if ctx.command is None:
                return
            if str(ctx.channel.type) == "public_thread":
                return
            await self.invoke(ctx)
        else:
            return

os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"

client=Bot()
client.owner_ids=ray
ray = ""

if __name__ == "__main__":
    bot = Bot()
    bot.run(ray, reconnect=True)