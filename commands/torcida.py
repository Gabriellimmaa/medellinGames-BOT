import asyncio
import json
import random
from time import time
from connection import MongoDB
from utils import COR, VERDE, VERMELHO, Emoji, checkUserTweet, date, dividirLista, format_hashtag, key_generator, open_account
from view.confirm import ConfirmTeam
from discord.ui import Button, View, Select
import discord

from view.torcida import CreateTorcida
from view.view import SelectViewDynamic

class PageViewTorcida(discord.ui.View):
    def __init__(self, author, torcida, page, options):
        super().__init__()
        self.value = None
        self.author = author
        self.torcida = torcida
        self.page = page
        self.options = options

    @discord.ui.button(label='<', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 1:
            self.page -= 1
        pageView = PageViewTorcida(self.author, self.torcida, self.page, self.options)
        pageView.add_item(Button(label=f"Página {self.page}", style=discord.ButtonStyle.primary, disabled=True))
        
        text = ""
        try:
            for x in self.options[self.page -1]:
                text += f'<@{x}>\n'
        except:
            text += "Nenhum membro encontrado"

        embed = discord.Embed(title=f"👥Torcida {self.torcida['_id']}",
                description=f"👑 **Lider:** <@{self.torcida['lider']}>\n🎯 **Pontuação:** `{self.torcida['ponto']}`\n🏆 **Vitórias:** `{self.torcida['vitoria']}`\n🥉 **Derrotas:** `{self.torcida['derrota']}`",
                color=COR)
        embed.add_field(name="Membros", value=f"{text}", inline=True)
        embed.add_field(name="\u200b", value="\u200b")
        await interaction.response.edit_message(embed=embed, view=pageView)


    @discord.ui.button(label='>', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.page += 1
        pageView = PageViewTorcida(self.author, self.torcida, self.page, self.options)
        pageView.add_item(Button(label=f"Página {self.page}", style=discord.ButtonStyle.primary, disabled=True))
        
        text = ""
        try:
            for x in self.options[self.page -1]:
                text += f'<@{x}>\n'
        except:
            text += "Nenhum membro encontrado"

        embed = discord.Embed(title=f"👥Torcida {self.torcida['_id']}",
                description=f"👑 **Lider:** <@{self.torcida['lider']}>\n🎯 **Pontuação:** `{self.torcida['ponto']}`\n🏆 **Vitórias:** `{self.torcida['vitoria']}`\n🥉 **Derrotas:** `{self.torcida['derrota']}`",
                color=COR)
        embed.add_field(name="Membros", value=f"{text}", inline=True)
        embed.add_field(name="\u200b", value="\u200b")
        await interaction.response.edit_message(embed=embed, view=pageView)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author == interaction.user

class ButtonAdd(discord.ui.Button):
    def __init__(self, author: discord.Member, channel: discord.ChannelType, torcida):
        super().__init__(label='+ Adicionar membro', style=discord.ButtonStyle.green, custom_id='add')
        self.value = None
        self.author = author
        self.channel = channel
        self.torcida = torcida

    async def callback(self, interaction: discord.Interaction):
        def check_msg(m):
            return m.author == self.author and m.channel == self.channel
        
        embed = discord.Embed(title=f"{Emoji().update} Adicionar membro", 
                            description=f"👥 **Torcida:** {self.torcida['_id']}\n👑 **Lider:** <@{self.torcida['lider']}>\n\n{Emoji().sirene} Mencione o **MEMBRO** que queira adicionar:", 
                            color=COR)
        embed.set_footer(text="Você tem 30 segundos para responder")
        await interaction.response.edit_message(embed=embed, view=None)
        try:
            r00 = await interaction.client.wait_for('message', check=check_msg, timeout=30)
            morador = r00.content
            await r00.delete()
            morador = morador.replace('<', '')
            morador = morador.replace('>', '')
            morador = morador.replace('@', '')
            member = interaction.client.get_user(int(morador))
            await open_account(member)
            memberdb = await MongoDB().dbuser.find_one({"_id": str(member.id)})
            if memberdb['torcida'] != False:
                embed = discord.Embed(title=f'',
                                description=f'{Emoji().errado} O membro {member.mention} já faz parte de outra torcida, sendo assim não podemos concluir está ação.',
                                color=VERMELHO)
                await interaction.edit_original_response(embed=embed, view=None)
                return
            
            confirmarMembro = View()
            botaoConfirmar = Button(label=f"Confirmar", emoji="✅", custom_id=f"confirmar", style=discord.ButtonStyle.green)
            confirmarMembro.add_item(botaoConfirmar)
            embed = discord.Embed(title=f"{Emoji().update} Adicionar membro", 
                            description=f"👥 **Torcida:** {self.torcida['_id']}\n👑 **Lider:** <@{self.torcida['lider']}>\n\n{Emoji().loading} {member.mention} confirme se deseja entrar na torcida...", 
                            color=COR)
            await interaction.edit_original_response(content=f"{self.author.mention} {member.mention}", embed=embed, view=confirmarMembro)

            async def confirmarMembro_callback(interaction: discord.Interaction):
                if interaction.user.id == member.id:
                    await interaction.response.defer()
                    confirmarMembro.stop()
                    memberdb = await MongoDB().dbuser.find_one({"_id": str(member.id)})
                    if memberdb['torcida'] != False:
                        embed = discord.Embed(title=f'',
                                        description=f'{Emoji().errado} O membro {member.mention} já faz parte de outra torcida, sendo assim não podemos concluir está ação.',
                                        color=VERMELHO)
                        await interaction.edit_original_response(embed=embed, view=None)
                        confirmarMembro.stop()
                        return
                    await MongoDB().dbuser.update_one({"_id": str(member.id)}, {"$set": {"torcida": self.torcida['_id']}})
                    await MongoDB().dbtorcida.update_one({"_id": self.torcida['_id']}, {"$push": {"membros": member.id}})
                    embed = discord.Embed(title=f"{Emoji().update} Adicionar membro", 
                            description=f"👥 **Torcida:** {self.torcida['_id']}\n👑 **Lider:** <@{self.torcida['lider']}>\n\n{Emoji().certo} {member.mention} foi adicionado com sucesso!", 
                            color=VERDE)
                    await interaction.edit_original_response(embed=embed, view=None)
                    confirmarMembro.stop()
                    return

            botaoConfirmar.callback = confirmarMembro_callback
            await confirmarMembro.wait()
        except asyncio.exceptions.TimeoutError:
            try:
                await r00.delete()
            except:
                pass
            embed = discord.Embed(title=f'',
                                description=f'{Emoji().errado} Seu tempo excede o limite de 30 segundos. Tente novamente.',
                                color=VERMELHO)
            await interaction.edit_original_response(embed=embed, view=None)
            self.stop()
            return
        except Exception as e:
            try:
                await r00.delete()
            except:
                pass
            embed = discord.Embed(title=f'',
                                description=f'{Emoji().errado} Mencione apenas um membro para adiciona-lo a torcida.',
                                color=VERMELHO)
            await interaction.edit_original_response(embed=embed, view=None)
            raise e
            self.stop()
            return

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author == interaction.user


class ButtonRemove(discord.ui.Button):
    def __init__(self, author: discord.Member, channel: discord.ChannelType, torcida):
        super().__init__(label='- Remover membro', style=discord.ButtonStyle.red, custom_id='remove')
        self.value = None
        self.author = author
        self.channel = channel
        self.torcida = torcida

    async def callback(self, interaction: discord.Interaction):
        def getName(valor):
            try:
                user = interaction.client.get_user(int(valor))
                return f"{user}"
            except:
                return valor

        listaItens = []
        for x in self.torcida['membros']:
            if x == self.torcida['lider']:
                continue
            nome = getName(x)
            torcida = self.torcida['_id']
            lista2 = [nome, x, torcida]
            listaItens.append(lista2)

        async def _cog_select_options(listaItens) -> list[discord.SelectOption]:
            options: list[discord.SelectOption] = []
            for valor in listaItens:
                options.append(discord.SelectOption(label=f"{valor[0]}", value=f"{valor[1]}:{valor[2]}"))
            return options

        if not listaItens:
            embed = discord.Embed(title=f'{Emoji().update} Remover membro',
                            description=f"👥 **Torcida:** {self.torcida['_id']}\n👑 **Lider:** <@{self.torcida['lider']}>\n\n{Emoji().sino} Não há membros para remover.",
                            color=COR)
            await interaction.response.edit_message(content=f"{self.author.mention}", embed=embed, view=None)
            return
        options = await _cog_select_options(listaItens)

        selectView = SelectViewDynamic(interaction.user, "removerMembro", options)
        embed = discord.Embed(title=f'{Emoji().update} Remover membro',
                            description=f"👥 **Torcida:** {self.torcida['_id']}\n👑 **Lider:** <@{self.torcida['lider']}>\n\n{Emoji().sirene} Selecione o **MEMBRO** que queira remover:",
                            color=COR)
        await interaction.response.edit_message(content=f"{self.author.mention}", embed=embed, view=selectView)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self.author == interaction.user

async def torcida(client: discord.Client, interaction: discord.Interaction, membro: discord.Member = None, nomeTorcida: str = None):
    author = interaction.user
    if membro is not None and nomeTorcida is not None:
        embed = discord.Embed(title=f'',
            description=f'{Emoji().errado} Argumentos inválidos\n\nUtilize: `/torcida <@membro>` ou `/torcida <nome torcida>`',
            color=VERMELHO)
        await interaction.edit_original_response(content=author.mention, embed=embed)
        return
    
    if membro == None:
        membro = author
    
    await interaction.response.defer()

    if nomeTorcida is not None:
        torcida = await MongoDB().dbtorcida.find_one({"_id": nomeTorcida})

        if torcida == None:
            embed = discord.Embed(title=f'{Emoji().update} Consultar torcida',
                description=f'{Emoji().errado} {membro.mention} A torcida `{nomeTorcida}` não existe\n\nUtilize: `/torcidas` para ver todas as torcidas',
                color=VERMELHO)
            await interaction.edit_original_response(content=membro.mention, embed=embed)
            return

        options = dividirLista(torcida['membros'], 10)
        page = 1 
        pageView = PageViewTorcida(membro, torcida, page, options)
        pageView.add_item(Button(label=f"Página {page}", style=discord.ButtonStyle.primary, disabled=True))
        if membro.id == torcida['lider']:
            pageView.add_item(ButtonAdd(membro, interaction.channel, torcida))
            pageView.add_item(ButtonRemove(membro, interaction.channel, torcida))
            # optionView = ViewOptionLider(user, interaction.channel, torcida)
        
        text = ""
        for x in options[page -1]:
            text += f'<@{x}>\n'
        if text == "":
            text += "Nenhum membro encontrado"

        embed = discord.Embed(title=f"👥Torcida {nomeTorcida}",
                description=f"👑 **Lider:** <@{torcida['lider']}>\n🎯 **Pontuação:** `{torcida['ponto']}`\n🏆 **Vitórias:** `{torcida['vitoria']}`\n🥉 **Derrotas:** `{torcida['derrota']}`",
                color=COR)
        embed.add_field(name="Membros", value=f"{text}", inline=True)
        embed.add_field(name="\u200b", value="\u200b")
        await interaction.edit_original_response(embed=embed, view=pageView)
        return
    await open_account(membro)
    data = await MongoDB().dbuser.find_one({"_id": str(membro.id)})
    if data['torcida'] == False and membro.id == author.id:
        criarTorcida = CreateTorcida(membro)
        embed = discord.Embed(title=f'{Emoji().sirene} Você não faz parte de nenhuma torcida',
                description=f'\n\u200b{Emoji().seta_azul} Você pode criar sua torcida ou entrar em alguma\n{Emoji().seta_azul} Apenas o lide da torcida pode adiciona-lo\n\u200b',
                color=COR)
        embed.add_field(name="Vantagens", value=f">>> Notícias Exclusivas\nClube Torcedor\nCalendario\nRanked\nDownloads\nCall Exclusiva ")
        embed.add_field(name="** **", value=f">>> Coletiva\nO dobro de pontos por atividade\nLoja Virtual Exclusiva\nPossibilidade de participar dos eventos presenciais\nPeneiras")
        await interaction.edit_original_response(content=author.mention, embed=embed, view=criarTorcida)
        await criarTorcida.wait()
    elif data['torcida'] == False:
        embed = discord.Embed(title=f'',
                description=f'{Emoji().seta_azul} {membro.mention} não faz parte de nenhuma torcida\n\nEle pode criar sua torcida ou entrar em alguma\nApenas o lider da torcida pode adiciona-lo\n\nUtilize: `/torcidas` para ver todas as torcidas e seus lideres',
                color=VERMELHO)
        await interaction.edit_original_response(embed=embed, view=None)
        return
    else:
        torcida = await MongoDB().dbtorcida.find_one({"_id": data['torcida']})

        options = dividirLista(torcida['membros'], 10)
        page = 1 
        pageView = PageViewTorcida(author, torcida, page, options)
        pageView.add_item(Button(label=f"Página {page}", style=discord.ButtonStyle.primary, disabled=True))
        if author.id == torcida['lider']:
            pageView.add_item(ButtonAdd(author, interaction.channel, torcida))
            pageView.add_item(ButtonRemove(author, interaction.channel, torcida))
            # optionView = ViewOptionLider(user, interaction.channel, torcida)
        
        text = ""
        for x in options[page -1]:
            text += f'<@{x}>\n'
        if text == "":
            text += "Nenhum membro encontrado"

        embed = discord.Embed(title=f"👥Torcida {torcida['_id']}",
                description=f"👑 **Lider:** <@{torcida['lider']}>\n🎯 **Pontuação:** `{torcida['ponto']}`\n🏆 **Vitórias:** `{torcida['vitoria']}`\n🥉 **Derrotas:** `{torcida['derrota']}`",
                color=COR)
        embed.add_field(name="Membros", value=f"{text}", inline=True)
        embed.add_field(name="\u200b", value="\u200b")
        await interaction.edit_original_response(embed=embed, view=pageView)
