import json
import random
from utils import checkUserTweet, date, format_hashtag, key_generator
from view.confirm import ConfirmTeam
import discord

COR = 0xf9eff8
VERDE = 0x66bb6a
VERMELHO = 0xef5350


async def join(client: discord.Client, interaction: discord.Interaction):
    emoji_certo = client.get_emoji(778443911974092840)
    emoji_sirene = client.get_emoji(854510226962907156)
    emoji_errado = client.get_emoji(778443911617708043)

    voice_state = interaction.user.voice

    if voice_state is None:
        print('Não esta conectado a nenhum canal de voz')
        return
    voice_channel = interaction.user.voice.channel
    voice_members = voice_channel.members
    random.shuffle(voice_members)
    
    # if len(voice_members) < 10:
    #     embed = discord.Embed(title='',
    #             description=f'{emoji_errado} {interaction.user.mention} Para sortear um time deve ter no minimo `10 membros` conectados a sua sala {voice_channel.mention}',
    #             color=VERMELHO)
    #     embed.set_author(name="Comando: /join")
    #     await interaction.response.send_message(embed=embed)
    #     return
    view = ConfirmTeam()
    embed = discord.Embed(title='Times Gerados', description=f'*Reaja conforme o time vencedor*', color=COR)
    # embed.add_field(name="Time A", value=f"{voice_members[0].mention}\n{voice_members[1].mention}\n{voice_members[2].mention}\n{voice_members[3].mention}\n{voice_members[4].mention}", inline=True)
    # embed.add_field(name="Time B", value=f"{voice_members[5].mention}\n{voice_members[6].mention}\n{voice_members[7].mention}\n{voice_members[8].mention}\n{voice_members[9].mention}", inline=True)
    embed.set_footer(text=f"{date()}")
    msg = await interaction.response.send_message(embed=embed, view=view)
    await view.wait()