import discord
import os
import time
from discord.ext import commands, tasks

client = commands.Bot(command_prefix="|", case_insensitive=True)
client.remove_command("help")

@client.event
async def on_ready():
    print("Online")

#Loading / Unloading Cogs
@client.command()
async def load(ctx, extension):
    if ctx.author.id == 160506586408812545:
        try:
            client.load_extension("Extension.{}".format(extension))
            await ctx.send("{} was Loaded.".format(extension))
        except discord.ext.commands.errors.ExtensionNotFound:
            await ctx.send("{} cannot be found!".format(extension))
        except discord.ext.commands.errors.ExtensionAlreadyLoaded:
            await ctx.send("{} is already loaded".format(extension))

@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 160506586408812545:
        try:
            client.unload_extension("Extension.{}".format(extension))
            await ctx.send("{} was Unloaded.".format(extension))
        except discord.ext.commands.errors.ExtensionNotLoaded:
            await ctx.send("{} was never loaded.".format(extension))

@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 160506586408812545:
        try:
            client.unload_extension("Extension.{}".format(extension))
        except discord.ext.commands.errors.ExtensionNotLoaded:
            await ctx.send("{} was never loaded.".format(extension))
            return
        client.load_extension("Extension.{}".format(extension))
        await ctx.send("{} was Reloaded.".format(extension))

for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension("Cogs.{}".format(filename[:-3]))

client.run('ODE0Mjk3MTk4ODkxMjM3NDI3.YDbzXQ.Cet7k0PToni4V-FvCSfGJNRkgl4')
