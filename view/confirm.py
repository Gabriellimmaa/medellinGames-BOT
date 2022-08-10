from discord.ext import commands
import discord
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
    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Você cancelou a ação do `/vip`", embed=None, view=None)
        self.value = False
        self.stop()
        
class ConfirmTeam(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Time A', style=discord.ButtonStyle.primary)
    async def confirmTeamA(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Aguarde ...", embed=None, view=None)
        self.value = True
        self.stop()

    @discord.ui.button(label='Time B', style=discord.ButtonStyle.primary)
    async def confirmTeamB(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(content="Aguarde ...", embed=None, view=None)
        self.value = True
        self.stop()


    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Cancelar', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(title='',
                description=f'{interaction.user.mention} Comando cancelado',
                color=VERMELHO)
        embed.set_author(name="Comando: /join")
        await interaction.response.edit_message(embed=embed, view=None)
        self.value = False
        self.stop()
        