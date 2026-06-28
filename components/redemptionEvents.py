from twitchio.ext import commands
import random

class RedemptionEvents(commands.Component):

    def __init__(self, bot):
        self.bot = bot

    # console log out all channel point redemptions
    @commands.Component.listener()
    async def event_custom_redemption_add(self, payload):
        print(f"{payload.user.name} redeemed {payload.reward.title}")