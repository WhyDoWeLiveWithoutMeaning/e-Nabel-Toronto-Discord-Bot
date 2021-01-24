#Imports

import discord
import requests
import json
import imaplib, email
import asyncio
import re
from discord.ext import commands

configuration = json.loads(open('Config.json', 'r').read())
imap_url = 'imap.gmail.com'

#Setting bot Intents
intents = discord.Intents.default()
intents.members = True

#Creating bot object
client = commands.Bot(command_prefix=configuration["prefix"], case_insensitive=True, intents=intents)
client.remove_command('help')

#Retreive Main Body Message
def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True)

#Remove HTML tags and string Formatters from text
def removeIt(tag):
    TAG_RE = re.compile(r'<.*?>')
    data = TAG_RE.sub('', tag)
    return data.replace('b"', "").replace('"', '').replace("\\r", "").replace("\\n", '').replace("b'", "").replace("'", '')


#config save function
def save_conf():
    open('Config.json', 'w').write(json.dumps(configuration))

#Getting Specific Roles
def check(ctx, roleName):
    #Gets all the roles in the server
    role = discord.utils.get(ctx.message.guild.roles, name=roleName)

    #If the user has that role
    if role in ctx.author.roles:
        return True
    else:
        return False

#The Help Command
@client.group(invoke_without_command=True)
async def help(ctx):
    embed = discord.Embed(title='Help', description='Use {}help [Command] for more information.\n<> -> Required\n[] -> Optional'.format(configuration["prefix"]))
    if check(ctx, "Leader"):
        embed.add_field(name="**Leader Commands**", value="`Purge`\n`Prefix`")
    await ctx.send(embed=embed)

@help.command()
async def purge(ctx):
    if check(ctx, "Leader"):
        embed = discord.Embed(title="Purge", description="Clear messages from chat.")
        embed.add_field(name="**Syntax**", value="{}purge <Number of Messages> [From User]".format(configuration["prefix"]))
        await ctx.send(embed=embed)

@help.command()
async def prefix(ctx):
    if check(ctx, "Leader"):
        embed = discord.Embed(title="Prefix", description="Change the bot prefix.")
        embed.add_field(name="**Syntax**", value="{}prefix <New Prefix>".format(configuration["prefix"]))
        await ctx.send(embed=embed)

#When Bot is Ready
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('{} | Building Hands'.format(configuration["prefix"])))
    client.loop.create_task(newsLetter())
    print('Bot is Online')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await client.process_commands(message)
#Every time a user joins
@client.event
async def on_member_join(member):
    channel = await client.fetch_channel(801909607928037480)
    await channel.send("Welcome <@{}> to the E-Nable Toronto Discord Server. :)".format(member.id))

#Clear command
@client.command(aliases=['purge'])
async def clear(ctx, numberOfMessages=None, user=None):
    #Check is the user is a Leader
    #If so continue
    if check(ctx, "Leader"):

        #Check if the number is specified.
        #If so continue
        if numberOfMessages != None:

            #Check if the user is specified.
            #If so continue
            if user != None:

                #Try turning user into valid user.
                try:
                    member = await client.fetch_user(int(user.replace('<', '') \
                    .replace('@', '') \
                    .replace('>', '') \
                    .replace('!', '')))
                except ValueError:
                    await ctx.send("Make sure the person is mentioned.")
                    return

                #local function to check if a users messages is from the member
                def is_user(m):
                    return m.author == member

                #Attempt to purge the messages
                try:
                    deleted = await ctx.channel.purge(limit=int(numberOfMessages), check=is_user)
                except ValueError:
                    await ctx.send("Please use a valid number.")
                    return

                #If successful return message.
                await ctx.send("{} Messages from {} have been deleted!".format(len(deleted), member.mention))
            else:

                #Attempt to deleted number of Messages
                try:
                    deleted = await ctx.channel.purge(limit=int(numberOfMessages))
                except ValueError:
                    await ctx.send("Please use a valid number.")
                    return

                #If successful reply.
                await ctx.send("{} Messages have been deleted!".format(len(deleted)))
        else:
            await ctx.send('Please Specify an Amount.')
    else:
        return

#Prefix command to Change the prefix
@client.command()
async def prefix(ctx, *newPrefix):

    #Check if user is leader
    if check(ctx, "Leader"):
        #Create new prefix
        prefix = "".join(newPrefix)

        #Temp save the old prefix
        prevPrefix = client.command_prefix

        #assign the new prefix
        client.command_prefix = prefix

        #save it in config file
        configuration["prefix"] = prefix
        save_conf()

        #update the bot and user.
        await client.change_presence(activity=discord.Game('{} | Building Hands'.format(configuration["prefix"])))
        await ctx.send("Prefix has been changed from {} to {}".format(prevPrefix, configuration["prefix"]))

async def newsLetter():
    #Prepare Channel
    channel = await client.fetch_channel(801911107768811530)
    def is_me(m):
        return m.author == client.user
    await channel.purge(limit=100, check=is_me)

    #Initial Letter
    num = 1

    #Loop forever
    while True:
        #Attempt to run the code
        try:
            #Log into email server
            con = imaplib.IMAP4_SSL(imap_url)
            con.login(configuration["email"], configuration["password"])

            #Get Only messages labeled as E-Nable Newsletter
            con.select('"E-Nable Newsletter"')

            #Get specific email
            result, data = con.fetch(bytes(f'{num}', 'utf-8'), '(RFC822)')

            #Turn message to string
            raw = email.message_from_bytes(data[0][1])
            await channel.send(removeIt(str(get_body(raw))))
            num += 1
        except TypeError: #If that email doesn't exist yet
            #Then do nothing and bottle it up
            None
        finally: #No matter what wait 24Hours to check again.
            await asyncio.sleep(86400)

#Run the bot through token
client.run(configuration["token"])
