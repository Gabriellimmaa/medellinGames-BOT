import asyncio
import json
from discord.ext import commands
import re
import discord
from connection import MongoDB
from discord.ui import Button, View, Select
from utils import COR, VERDE, VERMELHO, Emoji, date, open_account

class ContinueTorcida(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__()
        self.value = None
        self.user = user
        self.msg = None
        self.membros = []

    @discord.ui.button(label='+ Criar Torcida', style=discord.ButtonStyle.green)
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.user.id:
            user = interaction.user

            def check_msg(msg):
                return msg.author.id == user.id and msg.channel == interaction.channel

            embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                    description=f'{Emoji().seta_azul} Qual será o nome da sua torcida?',
                    color=COR)
            msg = await interaction.response.edit_message(content=user.mention, embed=embed, view=None)
            self.msg = msg
            r00 = await interaction.client.wait_for('message', check=check_msg)
            nomeTorcida = r00.content
            await r00.delete()
            
            if await MongoDB().dbtorcida.find_one({"_id": nomeTorcida}) is not None:
                embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                    description=f'{Emoji().errado} Já existe uma torcida com o nome de `{nomeTorcida}`',
                    color=VERMELHO)
                await interaction.edit_original_response(content=user.mention, embed=embed, view=None)   
                self.stop()
                return

            await MongoDB().dbtorcida.insert_one({"_id": nomeTorcida, "lider": self.user.id, "verificado": False, "ponto": 0, "vitoria": 0, "derrota": 0})
            embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                    description=f'{Emoji().seta_azul} Mencione os 10 membros de sua torcida (não pode se mencionar)\n\n*Exemplo: <@pessoa1> <@pessoa2> <@pessoa3> <@pessoa4>...*',
                    color=COR)
            embed.set_footer(text="Você tem 1 minuto para mencionar os membros")
            await interaction.edit_original_response(content=user.mention, embed=embed, view=None)
            try:
                r00 = await interaction.client.wait_for('message', check=check_msg, timeout=60.0)
            except asyncio.TimeoutError:
                await MongoDB().dbtorcida.delete_one({"_id": nomeTorcida})
                embed = discord.Embed(title='Criar torcida',
                    description=f'{Emoji().errado} Você demorou para mencionar os 10 membros da torcida',
                    color=VERMELHO)
                embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=f'{user.display_avatar}')
                await interaction.edit_original_response(embed=embed, view=None)
                self.stop()
                return

            messageResponse = r00.content
            await r00.delete()
            listaMencoes = re.split("\<([^\>]+)\>", messageResponse)
            listaMencoesManipulada = []
            for idMember in listaMencoes:
                try:    
                    idMember = idMember.strip('\n')
                    idMember = idMember.strip('\t') 
                    if idMember[0] == "@":
                        listaMencoesManipulada.append(int(idMember.strip("@")))
                        listaMencoes.remove(idMember)
                    else:
                        listaMencoes.remove(idMember)
                        pass
                except:
                    pass

            listaMencoesManipulada = sorted(set(listaMencoesManipulada))
            if user.id in listaMencoesManipulada:
                await MongoDB().dbtorcida.delete_one({"_id": nomeTorcida})
                embed = discord.Embed(title='Criar torcida',
                    description=f'{Emoji().errado} Você não pode se mencionar como membro do time',
                    color=VERMELHO)
                embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=f'{user.display_avatar}')
                await interaction.edit_original_response(embed=embed, view=None)
                self.stop()
                return

            listaMembrosTorcida = listaMencoesManipulada.copy()
            listaMembrosTorcida.append(interaction.user.id)
            if len(listaMencoesManipulada) < 10:
                await MongoDB().dbtorcida.delete_one({"_id": nomeTorcida})
                embed = discord.Embed(title='Criar torcida',
                    description=f'{Emoji().errado} Você não inseriu 10 membros ou inseriu membros repetidos',
                    color=VERMELHO)
                embed.set_author(name=f'{user.name}#{user.discriminator}', icon_url=f'{user.display_avatar}')
                await interaction.edit_original_response(embed=embed, view=None)
                self.stop()
                return
            
            confirmarMembro = View()
            botaoConfirmar = Button(label=f"Confirmar", emoji="✅", custom_id=f"confirmar", style=discord.ButtonStyle.green)
            confirmarMembro.add_item(botaoConfirmar)
            embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                description=f'Para prosseguir com a criação da torcida, ambos os membros devem confirmar sua entrada...',
                color=COR)
            var = ""
            for x in listaMencoesManipulada:
                var += f"<@{x}> "
            embed.add_field(name=f"{Emoji().loading} Aguardando confirmação de ", value=var)
            await interaction.edit_original_response(content=var, embed=embed, view=confirmarMembro)

            async def confirmarMembro_callback(interaction: discord.Interaction):
                if interaction.user.id in listaMencoesManipulada:
                    await open_account(interaction.user)
                    listaMencoesManipulada.remove(interaction.user.id)
                    if len(listaMencoesManipulada) == 0:
                        embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                            description=f'{Emoji().certo} A torcida `{nomeTorcida}` foi enviada para nossa administração, assim que ela for aprovada irá receber uma mensagem em sua DM\n\n> Confira seu status utilizando `/torcida`\n> Confira seus benefícios `/torcedor`',
                            color=VERDE)
                        await interaction.response.edit_message(embed=embed, view=None)

                        with open("config/config.json", "r") as f:
                            configJson = json.load(f)
                        canal_torcida = interaction.client.get_channel(int(configJson[str(interaction.guild.id)]['canal_torcida']))

                        var = ""
                        for x in listaMembrosTorcida:
                            var += f"<@{x}> "

                        embed = discord.Embed(title=f'{Emoji().update} Aprovar Torcida',
                                description=f'**Torcida:** {nomeTorcida}',
                                color=VERDE)
                        embed.add_field(name="Membros", value=var)
                        embed.add_field(name="** **", value=f"{Emoji().sino} Utilize `/aprovar {nomeTorcida}` para aprovar torcida", inline=False)
                        embed.set_footer(text=f'{date()}')        
                        msg = await canal_torcida.send(embed=embed)

                        await MongoDB().dbtorcida.update_one({"_id": nomeTorcida}, {"$set": {"membros": listaMembrosTorcida, "msgVerificar": msg.id}}, upsert=True)
                        confirmarMembro.stop()
                        return
                    var = ""
                    for x in listaMencoesManipulada:
                        var += f"<@{x}> "
                    embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                        description=f'Para prosseguir com a criação da torcida, ambos os membros devem confirmar sua entrada...',
                        color=COR)
                    embed.add_field(name=f"{Emoji().loading} Aguardando confirmação de ", value=var)
                    await interaction.response.edit_message(content=var, embed=embed, view=confirmarMembro)

            botaoConfirmar.callback = confirmarMembro_callback
            await confirmarMembro.wait()

    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.red)
    async def cancelar(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.user.id:
            user = interaction.user
            embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                description=f'{Emoji().errado} {user.mention} cancelou está ação',
                color=VERMELHO)
            await interaction.response.edit_message(embed=embed, view=None)
            self.stop()
            return

class CreateTorcida(discord.ui.View):
    def __init__(self, user: discord.Member):
        super().__init__()
        self.user = user

    @discord.ui.button(label='+ Criar Torcida', style=discord.ButtonStyle.green)
    async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id == self.user.id:
            user = interaction.user
            continuarView = ContinueTorcida(user)
            embed = discord.Embed(title=f'{Emoji().update} Criar torcida',
                    description=f'',
                    color=COR)
            embed.add_field(name="Regras para criar uma torcida", value=">>> Mínimo de 10 membros\n Proibido nome inapropriado\nToda torcida só é criada após a aprovação de um adm")
            await interaction.response.edit_message(content=user.mention, embed=embed, view=continuarView)
            await continuarView.wait()
            self.stop()