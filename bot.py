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
intents.voice_states = True
bot = commands.Bot(intents=intents, command_prefix='!')

# For now just have one user that we kick (_lajas's id)
user_id = 513915310496153600

@bot.event
async def on_ready():
    # guild = client.guilds[0]
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to Discord guild {guild.name}!')
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == user_id and after.channel and before.channel != after.channel:
        if True:
            print(f"Muting user {member.name} in channel {after.channel.name}")
            await member.edit(mute=True)
        else:
            print("kicking user from channel!")
            # TODO: kick user :)
        

bot.run(TOKEN)