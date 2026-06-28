# https://thepythoncode.com/article/control-keyboard-python
import keyboard

from twitchio.ext import commands

class TwitchPlays(commands.Component):

    def __init__(self, bot):
        self.bot = bot
    

    #  ------------------------------------------------------------------------------------------------------#

    ###----------###
    ### COMMANDS ###
    ###----------###

    # Let chat use keyboard inputs, in this case the spacebar. May need to impose limits on this later.
    @commands.command(name="jump")
    async def clap_command(self, ctx):
        keyboard.send("space")
