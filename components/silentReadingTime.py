import asyncio
import time
import random

from twitchio.ext import commands

class SilentReadingTime(commands.Component):

    def __init__(self, bot):
        self.bot = bot
        self.alert_parent_name = "Silent Reading Time"
        self.alert_1_id = None
        self.alert_2_id = None
        self.alert_3_id = None
        self.alert_4_id = None
        self.alert_5_id = None
        self.alert_6_id = None
        self.alert_7_id = None
        self.alert_8_id = None
        self.librarian_mode_timer = 0
        self.current_track = None
        self.load_ids()

    LIBRARIAN_MODE_MAX_TIME = 600 # 10 minute timer for silent reading

    #  ------------------------------------------------------------------------------------------------------#

    ###-----------###
    ### LISTENERS ###
    ###-----------###

    @commands.Component.listener()
    async def event_custom_redemption_add(self, payload):
        if payload.reward.title == "Silent Reading Time":

            # Show all alert boxes with varying delays between, then hide them in a similar fashion but backwards
            await self.show_all_alert_boxes()
            await asyncio.sleep(3.5)
            await self.hide_all_alert_boxes()
            await asyncio.sleep(10)

            # Activate librarian mode
            self.librarian_mode_timer = time.time() + self.LIBRARIAN_MODE_MAX_TIME
            self.play_classical_music()

    @commands.Component.listener()
    async def event_message(self, message):
        # Ignore the bot and me
        if message.chatter.id == self.bot.bot_id or message.chatter.broadcaster:
            return

        # Check timer
        if time.time() > self.librarian_mode_timer:
            return

        # timeout if any capitals in message
        if message.text != message.text.lower():
            await message.respond(f"/timeout {message.chatter.name} 30 no shouting in the library plink")
            await message.respond(f"{message.chatter.name} has been successfully shushed. please respect silent reading time. crunch")

    #  ------------------------------------------------------------------------------------------------------#

    ###---------###
    ### HELPERS ###
    ###---------###

    def show_alert_box(self, id):
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            id,
            True,
        )
        
        self.bot.obs_client.trigger_media_input_action(
            "SRT-alert-sound",
            "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART"
        )

    async def show_all_alert_boxes(self):
        self.show_alert_box(self.alert_1_id)
        await asyncio.sleep(3)
        self.show_alert_box(self.alert_2_id)
        await asyncio.sleep(2)
        self.show_alert_box(self.alert_3_id)
        await asyncio.sleep(1.5)
        self.show_alert_box(self.alert_4_id)
        await asyncio.sleep(1.5)
        self.show_alert_box(self.alert_5_id)
        await asyncio.sleep(2)
        self.show_alert_box(self.alert_6_id)
        await asyncio.sleep(1)
        self.show_alert_box(self.alert_7_id)
        await asyncio.sleep(0.5)
        self.show_alert_box(self.alert_8_id)

    async def hide_all_alert_boxes(self):
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_8_id,
            False,
        )
        await asyncio.sleep(0.8)
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_7_id,
            False,
        )
        await asyncio.sleep(0.4)
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_6_id,
            False,
        )
        await asyncio.sleep(0.2)
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_5_id,
            False,
        )
        await asyncio.sleep(0.2)
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_4_id,
            False,
        )
        await asyncio.sleep(0.1)
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_3_id,
            False,
        )
        await asyncio.sleep(0.1)
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_2_id,
            False,
        )
        await asyncio.sleep(0.1)
        self.bot.obs_client.set_scene_item_enabled(
            self.alert_parent_name,
            self.alert_1_id,
            False,
        )

    # Play one of three (currently) tracks in the background during 
    def play_classical_music(self):
        self.current_track = random.choice(["Classical-sound-1", "Classical-sound-2", "Classical-sound-3"])
        self.bot.obs_client.trigger_media_input_action(
            self.current_track,
            "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_RESTART"
        )
        asyncio.create_task(self.stop_music_after(self.LIBRARIAN_MODE_MAX_TIME))

    async def stop_music_after(self, seconds):
        await asyncio.sleep(seconds)

        if self.current_track is not None:
            self.bot.obs_client.trigger_media_input_action(
                self.current_track,
                "OBS_WEBSOCKET_MEDIA_INPUT_ACTION_STOP"
            )
            self.current_track = None

    def load_ids(self):
        items = self.bot.obs_client.get_group_scene_item_list(self.alert_parent_name)
        for item in items.scene_items:
            if item["sourceName"] == "SRT-alert-1":
                self.alert_1_id = item["sceneItemId"]
            elif item["sourceName"] == "SRT-alert-2":
                self.alert_2_id = item["sceneItemId"]
            elif item["sourceName"] == "SRT-alert-3":
                self.alert_3_id = item["sceneItemId"]
            elif item["sourceName"] == "SRT-alert-4":
                self.alert_4_id = item["sceneItemId"]
            elif item["sourceName"] == "SRT-alert-5":
                self.alert_5_id = item["sceneItemId"]
            elif item["sourceName"] == "SRT-alert-6":
                self.alert_6_id = item["sceneItemId"]
            elif item["sourceName"] == "SRT-alert-7":
                self.alert_7_id = item["sceneItemId"]
            elif item["sourceName"] == "SRT-alert-8":
                self.alert_8_id = item["sceneItemId"]