# https://www.geeksforgeeks.org/python/mouse-library-in-python
import asyncio
import pydirectinput

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
    @commands.command(name="space")
    async def space_kb_command(self, ctx):
        self.simulate_keypress("space", 0.2)
    
    @commands.command(name="click")
    async def leftclick_mb_command(self, ctx):
        pydirectinput.click()

    @commands.command(name="up")
    async def up_kb_command(self, ctx):
        self.simulate_keypress("w", 0.5)

    @commands.command(name="down")
    async def down_kb_command(self, ctx):
        self.simulate_keypress("s", 0.5)

    @commands.command(name="left")
    async def left_kb_command(self, ctx):
        self.simulate_keypress("a", 0.5)

    @commands.command(name="right")
    async def right_kb_command(self, ctx):
        self.simulate_keypress("d", 0.5)

    #  ------------------------------------------------------------------------------------------------------#

    ###---------###
    ### HELPERS ###
    ###---------###

    async def simulate_keypress(key, duration):
        pydirectinput.keyDown(key)
        await asyncio.sleep(duration)
        pydirectinput.keyUp(key)