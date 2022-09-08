import json
import random
from connection import MongoDB
from utils import COR, VERDE, VERMELHO, Emoji, checkUserTweet, date, format_hashtag, key_generator, open_account
from view.confirm import ConfirmTeam
import discord


async def aprovar(client: discord.Client, interaction: discord.Interaction, nomeTorcida):
    await open_account(interaction.user)
    await interaction.response.defer()
    user = interaction.user
    data = await MongoDB().dbtorcida.find_one({"_id": str(nomeTorcida)})
    if data is None:
        embed = discord.Embed(title=f'{Emoji().update} Aprovar torcida',
            description=f'{Emoji().errado} {user.mention} A torcida `{nomeTorcida}` não existe\n\nUtilize: `/torcidas` para ver todas as torcidas',
            color=VERMELHO)
        await interaction.edit_original_response(content=user.mention, embed=embed)
        return
    
    if data["verificado"] == True:
        embed = discord.Embed(title=f'{Emoji().update} Aprovar torcida',
            description=f'{Emoji().errado} {user.mention} A torcida `{nomeTorcida}` já foi aprovada\n\nUtilize: `/torcidas` para ver todas as torcidas',
            color=VERMELHO)
        await interaction.edit_original_response(content=user.mention, embed=embed)
        return
    

    validarTime = 0
    torcida = await MongoDB().dbtorcida.find_one({"_id": str(nomeTorcida)})
    for x in torcida['membros']:
        membro = await MongoDB().dbuser.find_one({"_id": str(x)})
        if membro['torcida'] != False:
            validarTime += 1

    if validarTime != 0:
        embed = discord.Embed(title=f'{Emoji().update} Aprovar torcida',
            description=f'{Emoji().errado} {user.mention} Um dos membros já faz parte de outra torcida, sendo assim não podemos concluir a aprovação desta torcida',
            color=VERMELHO)
        await interaction.edit_original_response(content=user.mention, embed=embed)
        return

    for x in torcida['membros']:
        await MongoDB().dbuser.update_one({"_id": str(x)}, {"$set": {"torcida": nomeTorcida}}, upsert=True)

    await MongoDB().dbtorcida.update_one({"_id": nomeTorcida}, {"$set": {"verificado": True}}, upsert=True)

    embed = discord.Embed(title=f"Aprovar torcida",
        description=f"{Emoji().certo} A torcida `{nomeTorcida}` foi aprovada com sucesso\n\nUtilize: `/torcidas` para ver todas as torcidas e seus lideres",
        color=VERDE)
    await interaction.edit_original_response(content=user.mention, embed=embed)
    return

