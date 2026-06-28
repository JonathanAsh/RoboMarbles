import asyncio
import random

from twitchio.ext import commands

class ClapCommands(commands.Component):

    def __init__(self, bot):
        self.bot = bot
        self.hands_apart_id = None
        self.hands_together_id = None
        self.clap_scene_id = None
        self.load_clap_ids()

    #  ------------------------------------------------------------------------------------------------------#

    ###-----------###
    ### VARIABLES ###
    ###-----------###

    claps = 0
    min_claps = 3
    max_claps = 7
    clap_running = False
    last_clap_sound = ""
    clap_sounds = [
        "ClapSound1",
        "ClapSound2",
        "ClapSound3",
        "ClapSound4",
        "ClapSound5",
        "ClapSound6",
        "ClapSound7",
    ]
    
    #  ------------------------------------------------------------------------------------------------------#

    ###----------###
    ### COMMANDS ###
    ###----------###

    # Let chat control a Tomodachi Life style pair of clapping hands.
    # The more people who type !clap, the longer it will clap for.
    # WARNING: Claps may not be synced, not sure how to do this accurately.
    @commands.command(name="clap")
    async def clap_command(self, ctx):
        await self.do_claps(random.randint(self.min_claps, self.max_claps))
    
    #  ------------------------------------------------------------------------------------------------------#

    ###-----------###
    ### LISTENERS ###
    ###-----------###

    # Listen for the Clap channel point redemption and play the clap
    @commands.Component.listener()
    async def event_custom_redemption_add(self, payload):
        if payload.reward.title == "Clap":
            await self.do_claps(random.randint(self.min_claps, self.max_claps))
    
    #  ------------------------------------------------------------------------------------------------------#

    ###---------###
    ### HELPERS ###
    ###---------###

    # Run actual logic so that it can be used both by chat and channel points
    async def do_claps(self, amount):

        # Don't overlap
        if self.clap_running:
            self.claps += amount
            return
        
        self.clap_running = True
        self.claps += amount

        try:
            while self.claps > 0:

                # Start with hands apart
                self.show_hands_apart()
                await asyncio.sleep(0.15)

                # Play random clap sound when hands come together (no two in a row)
                self.show_hands_together()
                sound = random.choice([s for s in self.clap_sounds if s != self.last_clap_sound])
                self.last_clap_sound = sound
                self.bot.obs_client.trigger_media_input_action(
                    sound,
                    "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART"
                )

                await asyncio.sleep(0.15)
                self.claps -= 1

        finally:
            self.hide_hands()
            self.clap_running = False

    # Hide closed hands, show open hands
    def show_hands_apart(self):

        self.bot.obs_client.set_scene_item_enabled(
            "ClapScene",
            self.hands_apart_id,
            True,
        )

        self.bot.obs_client.set_scene_item_enabled(
            "ClapScene",
            self.hands_together_id,
            False,
        )
        
    # Hide open hands, show closed hands
    def show_hands_together(self):

        self.bot.obs_client.set_scene_item_enabled(
            "ClapScene",
            self.hands_apart_id,
            False,
        )

        self.bot.obs_client.set_scene_item_enabled(
            "ClapScene",
            self.hands_together_id,
            True,
        )

    # Hide hands after clapping finished
    def hide_hands(self):
        self.bot.obs_client.set_scene_item_enabled(
            "ClapScene",
            self.hands_apart_id,
            False,
        )

        self.bot.obs_client.set_scene_item_enabled(
            "ClapScene",
            self.hands_together_id,
            False,
        )

    # Get clapping hand image IDs in case they change, along with ClapScene in Main View
    def load_clap_ids(self):

        # Hands ID (i think 55 and 56?)
        items = self.bot.obs_client.get_scene_item_list("ClapScene")
        for item in items.scene_items:
            if item["sourceName"] == "ClapApart":
                self.hands_apart_id = item["sceneItemId"]
            elif item["sourceName"] == "ClapTogether":
                self.hands_together_id = item["sceneItemId"]

        # Clap Scene ID (i think 67?)
        items = self.bot.obs_client.get_scene_item_list("Main View")
        for item in items.scene_items:
            if item["sourceName"] == "ClapScene":
                self.clap_scene_id = item["sceneItemId"]
