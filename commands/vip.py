import json
from utils import checkUserTweet, format_hashtag, key_generator
from view.confirm import Confirm
import discord
COR = 0xf9eff8
VERDE = 0x66bb6a
VERMELHO = 0xef5350

async def vip(client: discord.Client, interaction: discord.Interaction):
    emoji_certo = client.get_emoji(778443911974092840)
    emoji_sirene = client.get_emoji(854510226962907156)
    emoji_errado = client.get_emoji(778443911617708043)

    with open("data.json", "r") as f:
        data = json.load(f)

    newCode = key_generator()
    
    view = Confirm()
    embed = discord.Embed(title='',
                    description=f'Poste um tweet com nossa hashtag `{format_hashtag(data["hashtag"])}` e com o seguinte código `{newCode}`\n\n*Assim que postar volte aqui e confirme*',
                    color=COR)
    embed.set_author(name=f'{interaction.user.name}#{interaction.user.discriminator}',
                    icon_url=f'{interaction.user.avatar.url}')
    await interaction.response.send_message(embed=embed, ephemeral = True, view=view)
    await view.wait()
    
    if view.value:
        if checkUserTweet(interaction.user, data['hashtag']) is True:
            embed = discord.Embed(title='',
                    description=f'{emoji_certo} {interaction.user.mention} acabou de ativar seu plano `VIP` | *Utilize:* /vip',
                    color=VERDE)
            await interaction.channel.send(embed=embed)
        else:
            await interaction.followup.send(content=f"{interaction.user.mention} Não conseguimos encontrar seu tweet com nossa hashtag e seu código 😥", ephemeral = True)
