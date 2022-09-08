import json
from pydoc import cli
import random
from unittest import skip
from connection import MongoDB
from utils import COR, VERDE, VERMELHO, Emoji, checkUserTweet, date, dividirLista, format_hashtag, key_generator, open_account
from discord.ui import Button, View
import discord

from view.torcida import CreateTorcida

class PageViewTorcidas(discord.ui.View):
    def __init__(self, author, page):
        super().__init__()
        self.value = None
        self.author = author
        self.page = page

    @discord.ui.button(label='<', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
        pageView = PageViewTorcidas(self.author, self.page)
        pageView.add_item(Button(label=f"Página {self.page}", style=discord.ButtonStyle.primary, disabled=True))
        data = []   
        async for x in MongoDB().dbtorcida.find(limit=5, skip=(self.page-1)*5):
            data.append(x)
        text = ""
        for x in data:
            if x['verificado'] == False:
                text += Emoji().off
            else:
                text += Emoji().on
            text += f'{x["_id"]} | Lider: {interaction.client.get_user(x["lider"]).mention}\n'
        if text == "":
            text += "Nenhuma torcida encontrada"
        embed = discord.Embed(title="Lista Torcidas", description=f'>>> {text}', color=COR)
        embed.set_author(name=f'{interaction.user.name}#{interaction.user.discriminator}',
                        icon_url=f'{interaction.user.display_avatar}')
        await interaction.response.edit_message(embed=embed, view=pageView)


    @discord.ui.button(label='>', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        pageView = PageViewTorcidas(self.author, self.page)
        pageView.add_item(Button(label=f"Página {self.page}", style=discord.ButtonStyle.primary, disabled=True))
        data = []   
        async for x in MongoDB().dbtorcida.find(limit=5, skip=(self.page-1)*5):
            data.append(x)
        text = ""
        for x in data:
            if x['verificado'] == False:
                text += Emoji().off
            else:
                text += Emoji().on
            text += f'{x["_id"]} | Lider: {interaction.client.get_user(x["lider"]).mention}\n'
        if text == "":
            text += "Nenhuma torcida encontrada"
        embed = discord.Embed(title="Lista Torcidas", description=f'>>> {text}', color=COR)
        embed.set_author(name=f'{interaction.user.name}#{interaction.user.discriminator}',
                        icon_url=f'{interaction.user.display_avatar}')
        await interaction.response.edit_message(embed=embed, view=pageView)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author == interaction.user

async def torcidas(client: discord.Client, interaction: discord.Interaction):
    await open_account(interaction.user)
    user = interaction.user
    data = []
    page = 1
    async for x in MongoDB().dbtorcida.find(limit=5, skip=(page-1)*5):
        data.append(x)
    pageTorcidas = PageViewTorcidas(user, page)
    pageTorcidas.add_item(Button(label=f"Página {page}", style=discord.ButtonStyle.primary, disabled=True))
    text = ""
    for x in data:
        if x['verificado'] == False:
            text += Emoji().off
        else:
            text += Emoji().on
        text += f'{x["_id"]} | Lider: {client.get_user(x["lider"]).mention}\n'
    embed = discord.Embed(title=f"Lista Torcidas",
            description=f">>> {text}",
            color=COR)
    embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=f'{user.display_avatar}')
    await interaction.response.send_message(content=user.mention, embed=embed, view=pageTorcidas)

