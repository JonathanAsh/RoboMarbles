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
        pydirectinput.press("space")
    
    @commands.command(name="click")
    async def leftclick_mb_command(self, ctx):
        pydirectinput.click()

    @commands.command(name="up")
    async def up_kb_command(self, ctx):
        pydirectinput.keyDown("w")
        await asyncio.sleep(0.5)
        pydirectinput.keyUp("w")

    @commands.command(name="down")
    async def down_kb_command(self, ctx):
        pydirectinput.keyDown("s")
        await asyncio.sleep(0.5)
        pydirectinput.keyUp("s")

    @commands.command(name="left")
    async def left_kb_command(self, ctx):
        pydirectinput.keyDown("a")
        await asyncio.sleep(0.5)
        pydirectinput.keyUp("a")

    @commands.command(name="right")
    async def right_kb_command(self, ctx):
        pydirectinput.keyDown("d")
        await asyncio.sleep(0.5)
        pydirectinput.keyUp("d")
