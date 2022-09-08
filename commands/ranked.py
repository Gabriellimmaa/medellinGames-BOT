import json
import random
from utils import COR, VERDE, VERMELHO, Emoji, checkUserTweet, date, format_hashtag, key_generator, open_account
from view.confirm import ConfirmTeam
import discord


async def join(client: discord.Client, interaction: discord.Interaction):
    await open_account(interaction.user)
    voice_state = interaction.user.voice

    if voice_state is None:
        embed = discord.Embed(title='',
                description=f'{Emoji().errado} Você não está conectado a nenhum canal de voz',
                color=VERMELHO)
        embed.set_author(name=f'{interaction.user.name}#{interaction.user.discriminator}', icon_url=f'{interaction.user.display_avatar}')
        await interaction.response.send_message(embed=embed)
        return

    voice_channel = interaction.user.voice.channel
    voice_members = voice_channel.members
    # voice_members = ['1', '2', '3', '4', '5' ,'6' ,'7', '8']
    random.shuffle(voice_members)
    
    for membro in voice_members:
        await open_account(membro)

    if len(voice_members) < 8:
        embed = discord.Embed(title='',
                description=f'{Emoji().errado}  {interaction.user.mention} Para sortear um time deve ter no minimo `8 membros` conectados a sua sala {voice_channel.mention}',
                color=VERMELHO)
        embed.set_author(name=f'{interaction.user.name}#{interaction.user.discriminator}', icon_url=f'{interaction.user.display_avatar}')
        await interaction.response.send_message(embed=embed)
        return

    capitaoA = voice_members[random.randint(0, 3)]
    capitaoB = voice_members[random.randint(4, 7)]

    view = ConfirmTeam(capitaoA, capitaoB, voice_members)
    embed = discord.Embed(title='🕹️ Times Gerados', description=f'{Emoji().sino} *Após o jogo finalizar os dois capitães devem votar no time vencedor*', color=COR)
    embed.add_field(name="Time A", value=f"Capitão: {capitaoA.mention}\n> {voice_members[0].mention}\n> {voice_members[1].mention}\n> {voice_members[2].mention}\n> {voice_members[3].mention}\n\n{Emoji().loading} **Status:** `Aguardando voto...`", inline=True)
    embed.add_field(name="Time B", value=f"Capitão: {capitaoB.mention}\n> {voice_members[4].mention}\n> {voice_members[5].mention}\n> {voice_members[6].mention}\n> {voice_members[7].mention}\n\n{Emoji().loading} **Status:** `Aguardando voto...`", inline=True)
    embed.set_footer(text=f"{date()}")
    msg = await interaction.response.send_message(embed=embed, view=view)
    await view.wait()