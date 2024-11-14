import discord
from discord.ext import commands
from discord.ext.commands import Context
import json



async def get_prefix(self, message: discord.Message):
  with open('./Database/info.json', 'r') as f:
    p = json.load(f)
  if message.author.id in p["np"]:
    return commands.when_mentioned_or('$', '')(self,message)
  else:
      return commands.when_mentioned_or('$')(self,message)