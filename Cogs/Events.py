import discord
from discord.ext import commands

class EventCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = await self.client.get_channel(801909607928037480)
        await channel.send("Welcome {} to the E-Nable Toronto Discord Server. :)".format(member.mention))

def setup(client):
    client.add_cog(EventCog(client))
