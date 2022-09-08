import json
import discord
from discord import app_commands
from commands.torcida import torcida
from utils import *
from view.confirm import Confirm
import commands.vip as vipCommand
import commands.ranked as rankedCommand
import commands.torcida as torcidaCommand
import commands.aprovar as aprovarCommand
import commands.torcidas as torcidasCommand

config = getConfig()

guild_id = 1017300159673159730
COR = 0xf9eff8
VERDE = 0x66bb6a
VERMELHO = 0xef5350

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.all())
        self.synced = False 

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync(guild=discord.Object(id=guild_id))
            self.synced = True
        print(f"We have logged in as {self.user}.")


client = aclient()
tree = app_commands.CommandTree(client)

# guild specific slash command
@tree.command(guild=discord.Object(id=guild_id), name='vip', description='Pegar seu vip diario por tweet')
async def mainCommand(interaction: discord.Interaction):
    await vipCommand.vip(client, interaction)

@tree.command(guild=discord.Object(id=guild_id), name='join', description='Inicia um torneio')
async def mainCommand(interaction: discord.Interaction):
    await rankedCommand.join(client, interaction)

@tree.command(guild=discord.Object(id=guild_id), name='torcida', description='Consulta a torcida de um jogador ou cria uma nova')
async def mainCommand(interaction: discord.Interaction, membro: discord.Member = None, torcida: str = None):
    await torcidaCommand.torcida(client, interaction, membro, torcida)

@tree.command(guild=discord.Object(id=guild_id), name='aprovar', description='Aprova uma torcida')
async def self(interaction: discord.Interaction, nome: str):
    await aprovarCommand.aprovar(client, interaction, nome)

@tree.command(guild=discord.Object(id=guild_id), name='torcidas', description='Exibe a lista com todas as torcidas')
async def self(interaction: discord.Interaction):
    await torcidasCommand.torcidas(client, interaction)

client.run(config.discord_token)
