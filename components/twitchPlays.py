# https://thepythoncode.com/article/control-keyboard-python
# https://www.geeksforgeeks.org/python/mouse-library-in-python
import keyboard
import mouse

from twitchio.ext import commands

class TwitchPlays(commands.Component):

    def __init__(self, bot):
        self.bot = bot

    #  ------------------------------------------------------------------------------------------------------#

    ###----------###
    ### COMMANDS ###
    ###----------###

    # Let chat use keyboard + mouse inputs with commands
    # Currently there is spacebar, WASD, and the left mouse button
    # May need to impose limits on this later.
    @commands.command(name="jump")
    async def jump_kb_command(self, ctx):
        keyboard.send("space")
    
    @commands.command(name="click")
    async def leftclick_mb_command(self, ctx):
        mouse.click("left")

    @commands.command(name="up")
    async def up_kb_command(self, ctx):
        keyboard.send("w")

    @commands.command(name="down")
    async def down_kb_command(self, ctx):
        keyboard.send("s")

    @commands.command(name="left")
    async def left_kb_command(self, ctx):
        keyboard.send("a")

    @commands.command(name="right")
    async def right_kb_command(self, ctx):
        keyboard.send("d")
