import aiohttp
import asyncio
import time
import random
import os

from dotenv import load_dotenv
from twitchio.ext import commands

load_dotenv()

TWITCH_BOT_ID = os.getenv("TWITCH_BOT_ID")
TWITCH_OWNER_ID = os.getenv("TWITCH_OWNER_ID")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_BOT_ACCESS_TOKEN = os.getenv("TWITCH_BOT_ACCESS_TOKEN")

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
    EMOTES = [
        "marble98Shh",
        "marble98LOL",
        "marble98Trash",
        "marble98Explorer",
        "marble98Scary",
    ]
    SHUSH_MESSAGES = [
        "has been successfully shushed.",
        "has received a stern look from the librarian.",
        "has been escorted to the quiet reading corner.",
        "has been relocated to the children's section as they cannot behave.",
    ]

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

            # Give ten second warning
            await payload.respond('in ten seconds, all uses of capital letters will be punished until silent reading time is over.')
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

        # Exclude only channel emotes (for subs and mods only?), aka those with the prefix "marble98" in them
        text = message.text

        for emote in self.EMOTES:
            text = text.replace(emote, "")

        # Delete message if any capitals and scold
        if text != text.lower():
            await self.delete_message(message.id)
            await message.respond(f"{message.chatter.name.lower()} {random.choice(self.SHUSH_MESSAGES)} please respect silent reading time. crunch")

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

    async def delete_message(self, message_id: str):
        url = "https://api.twitch.tv/helix/moderation/chat"

        headers = {
            "Authorization": f"Bearer {TWITCH_BOT_ACCESS_TOKEN}",
            "Client-Id": TWITCH_CLIENT_ID,
        }

        params = {
            "broadcaster_id": TWITCH_OWNER_ID,
            "moderator_id": TWITCH_BOT_ID,
            "message_id": message_id,
        }

        async with aiohttp.ClientSession() as session:
            async with session.delete(
                url,
                headers=headers,
                params=params,
            ) as response:

                if response.status != 204:
                    print(await response.text())