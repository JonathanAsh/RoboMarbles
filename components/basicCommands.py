from twitchio.ext import commands

class BasicCommands(commands.Component):

    def __init__(self, bot):
        self.bot = bot
    
    #  ------------------------------------------------------------------------------------------------------#

    ###----------###
    ### COMMANDS ###
    ###----------###

    # TODO: add !emotes command since i turned off the streamelements bot

    # Switch to Be Right Back screen if mod or me
    @commands.command(name="brb")
    @commands.is_moderator()
    async def brb_command(self, ctx):
        self.bot.obs_client.set_current_program_scene("Be Right Back")

    # Switch to Main View screen if mod or me
    @commands.command(name="game")
    @commands.is_moderator()
    async def game_command(self, ctx):
        self.bot.obs_client.set_current_program_scene("Main View")