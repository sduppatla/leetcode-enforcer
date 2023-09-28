# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event
async def on_ready():
    # guild = client.guilds[0]
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to Discord guild {guild.name}!')
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

bot.run(TOKEN)