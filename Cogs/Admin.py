import discord
import datetime
from discord.ext import commands

class Administration(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['Clear'])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, Amount:int=100, user:discord.Member=None):
        def is_user(m):
            if user == None:
                return True
            return m.author == user

        amount_deleted = await ctx.channel.purge(limit=Amount, check=is_user)
        message = "{} messaged have been deleted!".format(len(amount_deleted)) if user == None else "{} message from {} have been deleted!".format(len(amount_deleted), user.name)
        await ctx.send(content=message)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.BadArgument):
            await ctx.send("Make sure you entered the correct values")
        else:
            raise(error)

def setup(client):
    client.add_cog(Administration(client))
