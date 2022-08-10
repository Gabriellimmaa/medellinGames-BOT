import json
import discord
from discord import app_commands
from twitter_data_search import checkUserTweet
from utils import *
from view.confirm import Confirm

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
async def tester(interaction: discord.Interaction):
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

client.run(config.discord_token)
