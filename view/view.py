from ast import Interactive
import asyncio
from decimal import Decimal
import json
from discord.ext import commands
from discord.ui import Button, View, Select
from discord.utils import get
import discord
from connection import MongoDB

from utils import COR, Emoji, dividirLista

class SelectViewDynamic(discord.ui.View):
    def __init__(self, author: discord.Member, command: str, options: list[discord.SelectOption]):
        super().__init__()
        count = 1
        self.author = author
        for x in dividirLista(options, 20):
            self.add_item(SelectCreateDynamic(author, command, count, x))
            count += 1

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author == interaction.user

class SelectCreateDynamic(discord.ui.Select):
    def __init__(self, author: discord.Member, command: str, count: int, options: list[discord.SelectOption]):
        super().__init__(placeholder=f"Página {count}", min_values=1, max_values=1, options=options)
        self.value = None
        self.author = author
        self.channel = None
        self.command = command

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.edit_message(content=f"{interaction.user.mention} {Emoji().loading} Estamos coletando suas informações...", embed=None, view=None)
        self.channel = interaction.channel
        if self.command == "removerMembro":
            member = int(self.values[0].split(':')[0])
            torcida = self.values[0].split(':')[1]
            await MongoDB().dbuser.update_one({"_id": str(member)}, {"$set": {"torcida": False}})
            await MongoDB().dbtorcida.update_one({"_id": torcida}, {"$pull": {"membros": member}})
            member = interaction.client.get_user(int(member))
            torcida = await MongoDB().dbtorcida.find_one({"_id": torcida})
            embed = discord.Embed(title=f"{Emoji().update} Remover membro", 
                    description=f"👥 **Torcida:** {torcida['_id']}\n👑 **Lider:** <@{torcida['lider']}>\n\n{Emoji().certo} {member.mention} foi removido com sucesso!", 
                    color=COR)
            await interaction.edit_original_response(content=interaction.user.mention, embed=embed, view=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author == interaction.user