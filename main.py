import os

import discord
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

def auth_check(user_id):
    if user_id not in [316965023404785674, 316965023404785674]:
        return False
    return True

@tree.command(
        name='vipboost',
        description='Make all members of community server a VIP.',
        guild=discord.Object(id=713038329851150366)
)
async def make_admin(interaction):
    all_members = interaction.guild.members
    if not auth_check(interaction.user.id):
        await interaction.response.send_message('You are not authorised to do this!')
        return
    
    boosted_members_info = open('boosted_members.txt', 'w')
    already_donated = open('already_vip.txt', 'w')

    for member in all_members:
        for role in member.roles:
            if role.name == 'VIP':
                already_donated.write(f'{member.id}\n')
        boosted_members_info.write(f'{member.id}\n')
        await member.add_roles(discord.utils.get(interaction.guild.roles, name='VIP'))
    boosted_members_info.close()
    already_donated.close()
    await interaction.response.send_message('Made everyone VIP!')


@tree.command(
        name='listallmembers',
        description='A test command to list all members in AB Community Server.',
        guild=discord.Object(id=713038329851150366)
)
async def list_all_members(interaction):
    if not auth_check(interaction.user.id):
        await interaction.response.send_message('You are not authorised to do this!')
        return
    all_members = interaction.guild.members
    print(len(all_members))
    print(all_members[0])
    await interaction.response.send_message('Command executed successfully :)')

@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=713038329851150366))
    print('Archive Bot Community Admin online!')


client.run(token=os.getenv('bot_token'))