from os.path import dirname,realpath
import sys
currentdir=dirname(realpath(__file__))
parentdir=dirname(currentdir)
sys.path.append(parentdir)
from env import *
from os import getpid as pid
from subprocess import run as shell
DISCORD_TOKEN=CONTROLLER
pidf=open("kill.bash","w+")
pidf.write(f"kill {pid()}")
pidf.close()
import discord,jishaku,platform,os
from discord.ext import commands
cmdpfx="bots."
client=commands.Bot(command_prefix=cmdpfx,case_insensitive=True,intents=discord.Intents.all())
token=DISCORD_TOKEN
hid=int(HID)
async def is_owner(ctx):
    return ctx.author.id==hid
async def procmsg(message,pfx,reqop=False,nopfx=False):
    if type(pfx)==str:
        pfx=[pfx]
    if nopfx:
        tmp=[]
        for i in pfx:
            tmp.append(f"{cmdpfx}{i}")
        pfx=tmp
    if reqop and not await is_owner(message):
        return False
    elif any([message.content.lower().replace(" ","").startswith(i) for i in pfx]):
        return True
    else:
        return False
@client.event
async def on_ready():
    global appinf,hid,pyver,discver,jskver,vers,startlat
    appinf=await client.application_info()
    pyver=platform.python_version()
    discver=discord.__version__
    jskver=jishaku.__version__
    vers={"Jishaku":jskver,"Discord.py":discver,"Python":pyver}
    startlat=int(client.latency*1000)
    print(f"We have logged in as {client.user}<@!{client.user.id}>")
    await client.change_presence(status="dnd",activity=discord.Game(f"Python {pyver} Discord.py {discver}"))
@client.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.errors.CommandNotFound):
        pass
@client.event
async def on_message(message):
    if message.author.id==client.user.id:
        return
    op=await is_owner(message)
    if await procmsg(message,["all.stop","bots.stop","all.close","bots.close","all.exit","bots.exit","all.logout","bots.logout","all.end","bots.end","all.kill","bots.kill"],reqop=True):
        await message.channel.send(content="Goodbye!")
        await client.close()
    if (message.content.startswith("all.token") or message.content.startswith("bots.token")) and message.author.id==hid:
        print(f"{message.author}<@!{message.author.id}> requested this bot's token and it was sent to them")
        await message.author.send(content=f"Here is the token you requested!\n```\n{token}\n```")
        await message.channel.send(content=":white_check_mark: Check your DMs! :white_check_mark:")
    if (message.content.startswith("all.token") or message.content.startswith("bots.token")) and message.author.id!=hid:
        print(f"{message.author}<@!{message.author.id}> requested this bot's token and it was not sent to them because they did not have the required permission")
        await message.channel.send(content=":x: You don't have the required permission. This incident has been logged. :x:")
    elif message.content=="all.tst":
        message.content="bots.tst"
    await client.process_commands(message)
@client.command()
async def tst(ctx):
    await ctx.send(content="I'm up!")
client.add_cog(jishaku.cog.Jishaku(bot=client))
client.run(token)