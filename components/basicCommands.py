from twitchio.ext import commands

class BasicCommands(commands.Component):

    def __init__(self, bot):
        self.bot = bot
    
    #  ------------------------------------------------------------------------------------------------------#

    ###----------###
    ### COMMANDS ###
    ###----------###

    # Switch to Be Right Back screen if mod or me
    @commands.command(name="brb")
    async def brb_command(self, ctx):
        if ctx.author.is_mod and ctx.author.name.lower() != "MarbleJelly".lower():
            return
        self.bot.obs_client.set_current_program_scene("Be Right Back")

    # Switch to Main View screen if mod or me
    @commands.command(name="game")
    async def game_command(self, ctx):
        if ctx.author.is_mod and ctx.author.name.lower() != "MarbleJelly".lower():
            return
        self.bot.obs_client.set_current_program_scene("Main View")