import json
import discord
from discord import app_commands
from utils import *
from view.confirm import Confirm
import commands.vip as vip
import commands.ranked as ranked

config = getConfig()

guild_id = 778405742835138561
COR = 0xf9eff8
VERDE = 0x66bb6a
VERMELHO = 0xef5350

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False  # we use this so the bot doesn't sync commands more than once

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:  # check if slash commands have been synced
            # guild specific: leave blank if global (global registration can take 1-24 hours)
            await tree.sync(guild=discord.Object(id=guild_id))
            self.synced = True
        print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)

# guild specific slash command
@tree.command(guild=discord.Object(id=guild_id), name='vip', description='Pegar seu vip diario')
async def mainCommand(interaction: discord.Interaction):
    await vip.vip(client, interaction)

@tree.command(guild=discord.Object(id=guild_id), name='join', description='Sorteia um time 5x5 em call')
async def mainCommand(interaction: discord.Interaction):
    await ranked.join(client, interaction)

client.run(config.discord_token)
