# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import leetcode_submission_retriever

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

lsr = leetcode_submission_retriever.LeetcodeSubmissionRetriever()
leetcode_username = "sduppatla"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(intents=intents, command_prefix='!')

# For now just have one user that we kick (_lajas's id)
user_id = 513915310496153600

@bot.event
async def on_ready():
    guild = discord.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to Discord guild {guild.name}!')
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_voice_state_update(member, before, after):
    # Mute user if joining voice channel and leetcode needs to be enforced
    if member.id == user_id and before.channel != after.channel and after.channel != None:
        if lsr.should_enforce(leetcode_username):
            await member.edit(mute=True)
        else:
            await member.edit(mute=False)
        

bot.run(TOKEN)