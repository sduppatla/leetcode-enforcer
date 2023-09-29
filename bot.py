# bot.py
import os

import disnake
from disnake.ext import commands
from disnake import CategoryChannel, Color
from disnake import Permissions, PermissionOverwrite
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
        # Mute user whenever joining voice channel
        if lsr.should_enforce(leetcode_username):
            print(f"Muted member {member.name}")
            await member.edit(mute=True)
        elif after.mute:
            print(f"Unmuted member {member.name}")
            await member.edit(mute=False)

# 86400 -- one day -- 60 secs * 60 mins * 24 hrs 
@bot.slash_command(description="Enforces that user has submitted a leetcode in the last {enforce_seconds} seconds")
async def enforce_leetcode(inter, discord_user: disnake.User, enforce_seconds: int = 86400):
    guild = disnake.utils.get(bot.guilds, name=GUILD)
    member = guild.get_member(discord_user.id)
    role_ids = list(map(lambda role: role.id, filter(lambda role: role.name != "@everyone", member.roles)))
    leetcode_username = users.get_leetcode_username_from_discord(member.id)

    if not leetcode_username:
        await inter.response.send_message(f"User {discord_user.name} is not registered... can not enforce.")
        return

    if lsr.should_enforce(leetcode_username, enforce_seconds):
        # Remove all current roles and add leetcode enforcer role.
        leetcode_rid = users.get_leetcode_rid()
        await member.edit(roles=[guild.get_role(leetcode_rid)])
        await inter.response.send_message(f"User {discord_user.name} is restricted until a new leetcode is submitted.")
    else:
        # Restore previous roles and remove leetcode enforcer role.
        rids = users.get_user_roles(discord_user.id)
        roles = list(map(lambda rid: guild.get_role(rid), rids))
        await member.edit(roles=roles)
        await inter.response.send_message(f"User {discord_user.name} has done their leetcode and is now unrestricted :)")

        
@bot.slash_command(description="Register a user's discord id with their leetcode username")
@commands.default_member_permissions(administrator=True)
async def register(inter, discord_user: disnake.User, leetcode_username: str):
    print(f"Registering discord user: {discord_user.id} with leetcode username: {leetcode_username}")
    guild = disnake.utils.get(bot.guilds, name=GUILD)
    member = guild.get_member(discord_user.id)
    role_ids = list(map(lambda role: role.id, filter(lambda role: role.name != "@everyone", member.roles)))
    users.register_user(discord_user.id, leetcode_username, role_ids)
    await inter.response.send_message(f"Registered user {discord_user.name} with leetcode user {leetcode_username}")

@bot.slash_command(setup="Creates a leetcode-violator role with no permissions to apply to user")
@commands.default_member_permissions(administrator=True)
async def setup(inter):
    guild = disnake.utils.get(bot.guilds, name=GUILD)

    # If we already have a leetcode-violator role setup is likely done.
    for role in guild.roles:
        if role.name == "leetcode-violator":
            await inter.response.send_message(f"leetcode-violator role already exists.. setup likely done")
            return

    print(f"Creating leetcode-violator role for guild {guild.name}")
    role = await guild.create_role(name="leetcode-violator",
                            permissions=Permissions(view_channel=True,
                                                    read_message_history=True),
                            color=Color.dark_gold(),
                            hoist=True,
                            mentionable=True)
    users.register_leetcode_role(role.id)
    
    print(f"Creating leetcode-violators channel for guild {guild.name}")
    # Allow leetcode-violators to send messages in their channel 
    po = PermissionOverwrite(send_messages=True)
    await guild.create_text_channel(name="leetcode-violators",
                                    overwrites={role: po})
    await inter.response.send_message("Setup finished successfully, created role: leetcode-violator")

@bot.slash_command(setup="Creates a leetcode-violator role with no permissions to apply to user")
@commands.default_member_permissions(administrator=True)
async def cleanup(inter):
    guild = disnake.utils.get(bot.guilds, name=GUILD)
    for role in guild.roles:
        if role.name == "leetcode-violator":
            await role.delete()
    users.unregister_leetcode_role()
    for channel in guild.channels:
        if channel.name == "leetcode-violators":
            await channel.delete()
    await inter.response.send_message("Cleanup finished successfully.")

bot.run(TOKEN)