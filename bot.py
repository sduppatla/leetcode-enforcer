# bot.py
import os

import disnake
from disnake.ext import commands
from dotenv import load_dotenv

import leetcode_submission_retriever
import users

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

lsr = leetcode_submission_retriever.LeetcodeSubmissionRetriever()

users = users.UserStorage()

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(intents=intents, command_prefix='!')

@bot.event
async def on_ready():
    guild = disnake.utils.get(bot.guilds, name=GUILD)
    print(f'{bot.user} has connected to Discord guild {guild.name}!')
    
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')

@bot.event
async def on_voice_state_update(member, before, after):
    leetcode_username = users.get_leetcode_username_from_discord(member.id)
    # If user is not registered with bot skip...
    if not leetcode_username:
        return
    # Mute user if joining voice channel and leetcode needs to be enforced
    if before.channel != after.channel and after.channel != None:
        if lsr.should_enforce(leetcode_username):
            print(f"Muted member {member.name}")
            await member.edit(mute=True)
        else:
            print(f"Unmuted member {member.name}")
            await member.edit(mute=False)
        
@bot.slash_command(description="Register a user's discord id with their leetcode username")
async def register(inter, discord_user: disnake.User, leetcode_username: str):
    print(f"Registering discord user: {discord_user.id} with leetcode username: {leetcode_username}")
    users.register_user(discord_user.id, leetcode_username)
    await inter.response.send_message(f"Registered user {discord_user.name} with leetcode user {leetcode_username}")

bot.run(TOKEN)