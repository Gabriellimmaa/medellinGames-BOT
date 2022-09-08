from discord.ext import commands
import discord
from connection import MongoDB

from utils import Emoji, date, open_account
COR = 0xf9eff8
VERDE = 0x66bb6a
VERMELHO = 0xef5350

# Define a simple View that gives us a confirmation menu
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label='Confirmar', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Aguarde ...", embed=None, view=None)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Você cancelou a ação do `/vip`", embed=None, view=None)
        self.value = False
        self.stop()
        
class ConfirmPadrao(discord.ui.View):
    def __init__(self, user: discord.Member, timeoutValue: int = None):
        if timeoutValue is None:
            super().__init__()
        else:
            super().__init__(timeout=timeoutValue)
        self.value = None
        self.author = user

    async def on_timeout(self) -> None:
        return self.value

    @discord.ui.button(label='✔', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author == interaction.user:
            self.value = True
            self.stop()

    @discord.ui.button(label='✖', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.author == interaction.user:            
            self.value = False
            self.stop()

class ConfirmTeam(discord.ui.View):
    def __init__(self, capitaoA: discord.Member, capitaoB: discord.Member, voice_members: list):
        super().__init__()
        self.value = None
        self.voice_members = voice_members
        self.capitaoA = capitaoA
        self.capitaoB = capitaoB
        self.votoCapitaoA = 'Aguardando voto...'
        self.votoCapitaoB = 'Aguardando voto...'
        self.checkVoto = []


    @discord.ui.button(label='Time A', style=discord.ButtonStyle.primary)
    async def confirmTeamA(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.capitaoA.id:
            self.votoCapitaoA = 'Time A'

        if interaction.user.id == self.capitaoB.id:
            self.votoCapitaoB = 'Time A'
            interaction.response.is_done()

        if interaction.user.id == self.capitaoA.id or interaction.user.id == self.capitaoB.id:
            embed = discord.Embed(title='🕹️ Times Gerados', description=f'{Emoji().sino} *Após o jogo finalizar os dois capitães devem votar no time vencedor*', color=COR)
            embed.add_field(name="Time A", value=f"Capitão: {self.capitaoA.mention}\n> {self.voice_members[0].mention}\n> {self.voice_members[1].mention}\n> {self.voice_members[2].mention}\n> {self.voice_members[3].mention}\n\n{Emoji().loading} **Status:** `{self.votoCapitaoA}`", inline=True)
            embed.add_field(name="Time B", value=f"Capitão: {self.capitaoB.mention}\n> {self.voice_members[4].mention}\n> {self.voice_members[5].mention}\n> {self.voice_members[6].mention}\n> {self.voice_members[7].mention}\n\n{Emoji().loading} **Status:** `{self.votoCapitaoB}`", inline=True)
            embed.set_footer(text=f"{date()}")
            await interaction.response.edit_message(embed=embed)
            if self.votoCapitaoA == 'Time A' and self.votoCapitaoB == 'Time A':
                self.value = 'A'
                qtdPontos = []
                for x in range(0, 4):
                    data = await MongoDB().dbuser.find_one({"_id": str(self.voice_members[x].id)})
                    pontosUpdate = 100
                    if data['vip'] == True or data['torcida'] != False:
                        pontosUpdate *= 2 
                    qtdPontos.append(pontosUpdate)
                    if data['torcida'] != False:
                        await MongoDB().dbtorcida.update_one({"_id": data["torcida"]}, {"$inc": {"ponto": pontosUpdate, "vitoria": 1}})
                    await MongoDB().dbuser.update_one({"_id": str(self.voice_members[x].id)}, {"$inc": {"ponto": pontosUpdate, "vitoria": 1}}, upsert=True)
                for x in range(4, 8):
                    data = await MongoDB().dbuser.find_one({"_id": str(self.voice_members[x].id)})
                    if data['torcida'] != False:
                        await MongoDB().dbtorcida.update_one({"_id": data["torcida"]}, {"$inc": {"derrota": 1}})
                    await MongoDB().dbuser.update_one({"_id": str(self.voice_members[x].id)}, {"$inc": {"derrota": 1}}, upsert=True)
                embed = discord.Embed(title='🕹️ Jogo finalizado', description=f'{Emoji().seta_azul} Time A foram os vencedores', color=VERDE)
                embed.add_field(name="Time A", value=f"Capitão: {self.capitaoA.mention}\n> {Emoji().on} {self.voice_members[0]} +{qtdPontos[0]}\n> {Emoji().on} {self.voice_members[1]} +{qtdPontos[1]}\n> {Emoji().on} {self.voice_members[2]} +{qtdPontos[2]}\n> {Emoji().on} {self.voice_members[3]} +{qtdPontos[3]}", inline=True)
                embed.add_field(name="Time B", value=f"Capitão: {self.capitaoB.mention}\n> {Emoji().off} {self.voice_members[4]}\n> {Emoji().off} {self.voice_members[5]}\n> {Emoji().off} {self.voice_members[6]}\n> {Emoji().off} {self.voice_members[7]}", inline=True)
                embed.add_field(name="\u200b", value="🎉 *Parabéns a todos os jogadores*", inline=False)
                embed.set_footer(text=f"{date()}")
                await interaction.edit_original_response(embed=embed, view=None)
                interaction.response.is_done()
                self.stop()
                
    @discord.ui.button(label='Time B', style=discord.ButtonStyle.primary)
    async def confirmTeamB(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.capitaoA.id:
            self.votoCapitaoA = 'Time B'

        if interaction.user.id == self.capitaoB.id:
            self.votoCapitaoB = 'Time B'

        if interaction.user.id == self.capitaoA.id or interaction.user.id == self.capitaoB.id:
            embed = discord.Embed(title='🕹️ Times Gerados', description=f'{Emoji().sino} *Após o jogo finalizar os dois capitães devem votar no time vencedor*', color=COR)
            embed.add_field(name="Time A", value=f"Capitão: {self.capitaoA.mention}\n> {self.voice_members[0].mention}\n> {self.voice_members[1].mention}\n> {self.voice_members[2].mention}\n> {self.voice_members[3].mention}\n\n{Emoji().loading} **Status:** `{self.votoCapitaoA}`", inline=True)
            embed.add_field(name="Time B", value=f"Capitão: {self.capitaoB.mention}\n> {self.voice_members[4].mention}\n> {self.voice_members[5].mention}\n> {self.voice_members[6].mention}\n> {self.voice_members[7].mention}\n\n{Emoji().loading} **Status:** `{self.votoCapitaoB}`", inline=True)
            embed.set_footer(text=f"{date()}")
            await interaction.response.edit_message(embed=embed)
            if self.votoCapitaoA == 'Time B' and self.votoCapitaoB == 'Time B':
                self.value = 'Time B'
                qtdPontos = []
                for x in range(4, 8):
                    data = await MongoDB().dbuser.find_one({"_id": str(self.voice_members[x].id)})
                    pontosUpdate = 100
                    if data['vip'] == True or data['torcida'] != False:
                        pontosUpdate *= 2 
                    qtdPontos.append(pontosUpdate)
                    if data['torcida'] != False:
                        await MongoDB().dbtorcida.update_one({"_id": data["torcida"]}, {"$inc": {"ponto": pontosUpdate, "vitoria": 1}})
                    await MongoDB().dbuser.update_one({"_id": str(self.voice_members[x].id)}, {"$inc": {"ponto": pontosUpdate, "vitoria": 1}})
                for x in range(0, 4):
                    data = await MongoDB().dbuser.find_one({"_id": str(self.voice_members[x].id)})
                    if data['torcida'] != False:
                        await MongoDB().dbtorcida.update_one({"_id": data["torcida"]}, {"$inc": {"derrota": 1}})
                    await MongoDB().dbuser.update_one({"_id": str(self.voice_members[x].id)}, {"$inc": {"derrota": 1}})
                embed = discord.Embed(title='🕹️ Jogo finalizado', description=f'{Emoji().seta_azul} Time B foram os vencedores', color=VERDE)
                embed.add_field(name="Time A", value=f"Capitão: {self.capitaoA.mention}\n> {Emoji().off} {self.voice_members[0]}\n> {Emoji().off} {self.voice_members[1]}\n> {Emoji().off} {self.voice_members[2]}\n> {Emoji().off} {self.voice_members[3]}", inline=True)
                embed.add_field(name="Time B", value=f"Capitão: {self.capitaoB.mention}\n> {Emoji().on} {self.voice_members[4]} +{qtdPontos[0]}\n> {Emoji().on} {self.voice_members[5]} +{qtdPontos[1]}\n> {Emoji().on} {self.voice_members[6]} +{qtdPontos[2]}\n> {Emoji().on} {self.voice_members[7]} +{qtdPontos[3]}", inline=True)
                embed.add_field(name="\u200b", value="🎉 *Parabéns a todos os jogadores*", inline=False)
                embed.set_footer(text=f"{date()}")
                await interaction.edit_original_response(embed=embed, view=None)
                interaction.response.is_done()
                self.stop()


    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.capitaoA.id or interaction.user.id == self.capitaoB.id:
            embed = discord.Embed(title='',
                description=f'{Emoji().errado} Comando `/join` cancelado',
                color=VERMELHO)
            embed.set_author(name=f'{interaction.user.name}#{interaction.user.discriminator}', icon_url=f'{interaction.user.display_avatar}')
            await interaction.edit_original_response(embed=embed, view=None)
            interaction.response.is_done()
            self.stop()
        