from __future__ import annotations

import asyncio
import os

from dotenv import load_dotenv
from twitchio import eventsub
from twitchio.ext import commands
import obsws_python as obs

from components.clapCommands import ClapCommands
from components.twitchPlays import TwitchPlays
from components.basicCommands import BasicCommands
from components.redemptionEvents import RedemptionEvents

load_dotenv()

TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")
TWITCH_BOT_ID = os.getenv("TWITCH_BOT_ID")
TWITCH_OWNER_ID = os.getenv("TWITCH_OWNER_ID")
TWITCH_BOT_ACCESS_TOKEN = os.getenv("TWITCH_BOT_ACCESS_TOKEN")
TWITCH_BOT_REFRESH_TOKEN = os.getenv("TWITCH_BOT_REFRESH_TOKEN")
TWITCH_OWNER_ACCESS_TOKEN = os.getenv("TWITCH_OWNER_ACCESS_TOKEN")
TWITCH_OWNER_REFRESH_TOKEN = os.getenv("TWITCH_OWNER_REFRESH_TOKEN")
OBS_HOST = os.getenv("OBS_HOST", "localhost")
OBS_PORT = int(os.getenv("OBS_PORT", "4455"))
OBS_PASSWORD = os.getenv("OBS_PASSWORD")

# TODO: make twitch plays pokemon thingy, which needs:
#         - make new channel point redemption for blocking my input (?)
#         - read chat inputs and input them via python

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            client_id=TWITCH_CLIENT_ID,
            client_secret=TWITCH_CLIENT_SECRET,
            bot_id=TWITCH_BOT_ID,
            owner_id=TWITCH_OWNER_ID,
            prefix="!",
        )

        self.obs_client = obs.ReqClient(
            host=OBS_HOST,
            port=OBS_PORT,
            password=OBS_PASSWORD,
        )

    async def setup_hook(self) -> None:
        # Two tokens, one for chat appearance as robomarbles and another for reading channel point redemptions (need to be channel owner)
        await self.add_token(TWITCH_BOT_ACCESS_TOKEN, TWITCH_BOT_REFRESH_TOKEN)
        await self.add_token(TWITCH_OWNER_ACCESS_TOKEN, TWITCH_OWNER_REFRESH_TOKEN)

        # Load the commands from components
        await self.add_component(BasicCommands(self))
        await self.add_component(ClapCommands(self))
        await self.add_component(TwitchPlays(self))
        await self.add_component(RedemptionEvents(self))

        # Watch every chat message
        await self.subscribe_websocket(
            payload=eventsub.ChatMessageSubscription(
                broadcaster_user_id=TWITCH_OWNER_ID,
                user_id=TWITCH_BOT_ID,
            )
        )

        # Watch every channel point redemption
        await self.subscribe_websocket(
            payload=eventsub.ChannelPointsRedeemAddSubscription(
                broadcaster_user_id=TWITCH_OWNER_ID,
            )
        )

    async def event_ready(self):
        print(f"Logged in as bot user ID: {TWITCH_BOT_ID}")
        print(f"Listening to channel user ID: {TWITCH_OWNER_ID}")
        print("Registered commands:")
        for name in self.commands:
            print(name)

    async def event_message(self, payload):
        chatter = payload.chatter.name
        text = payload.text

        # Log every chat message in console
        print(f"{chatter}: {text}")
        await self.process_commands(payload)

async def main():
    async with Bot() as bot:
        await bot.start()

if __name__ == "__main__":
    asyncio.run(main())