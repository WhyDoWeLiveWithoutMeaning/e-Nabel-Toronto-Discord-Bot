import discord
import datetime
from discord.ext import commands

class HelpCommand(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True)
    async def help(self, ctx):
        embed = discord.Embed(title="Help", description="Use |Help [Command]\n[] - > Optional\n{} - > Required")
        embed.add_field(name="User", value="""
        `Help` - > This
        """)
        if ctx.author.guild_permissions.manage_messages:
            embed.add_field(name="Admin", inline=False, value="""
            `Purge` - > Purge Messages
            """)
        embed.set_footer(text="E-Nable Toronto")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @help.command()
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        embed = discord.Embed(title="Purge", description="")
        embed.add_field(name="How to Use", value="|Purge [Amount] [User]")
        await ctx.send(embed=embed)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.MissingPermissions):
            return
        else:
            raise(error)


def setup(client):
    client.add_cog(HelpCommand(client))
