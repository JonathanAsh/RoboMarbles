from twitchio.ext import commands

class BasicCommands(commands.Component):

    def __init__(self, bot):
        self.bot = bot
    
    #  ------------------------------------------------------------------------------------------------------#

    ###----------###
    ### COMMANDS ###
    ###----------###

    # Lists all available commands
    # Note: could i do this with the thing in bot.py which lists them?
    @commands.command(name="help")
    async def help_command(self, ctx):
        await ctx.send("Current commands: !emotes to list all emotes, !discord for a link to the discord, !controls to press my buttons")

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

    # Display all (7tv) emotes in one message
    @commands.command(name="emotes")
    async def emotes_command(self, ctx):
        await ctx.send("GIGACHAD NOOOO catJAM catKISS OMEGALUL donowall modCheck SUSSY KEKW LETSGO RAGEY Pog classic HUH WHAT ICANT LETHIMCOOK Nerd D: CAUGHT Jigglin YesYes Amogus hi happie AAAA NOTED veryCat Kissahomie Cinema MODS monkaS crunch POGGIES plink PauseChamp Sadge")
    
    # Posts link to the discord
    @commands.command(name="discord")
    async def discord_command(self, ctx):
        await ctx.send("https://discord.gg/4UaX9kJvd6")

    # Displays just the input control commands
    @commands.command(name="controls")
    async def controls_command(self, ctx):
        await ctx.send("!jump to hit spacebar, !up/down/left/right for WASD, !click to left click")