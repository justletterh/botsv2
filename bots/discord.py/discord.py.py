import discord,jishaku,platform,os
from discord.ext import commands
cmdpfx="py."
client=commands.Bot(command_prefix=cmdpfx,case_insensitive=True,intents=discord.Intents.all())
token=os.environ['DISCORD_TOKEN']
hid=int(os.environ['HID'])
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
    if await procmsg(message,["py.ver","all.ver","py.version","all.version"],reqop=False):
        cont=["```"]
        for v in vers:
            cont.append(f"{v} Version:{(25-len(v))*' '}{vers[v]}")
        cont.append("```")
        await message.channel.send(content="\n".join(cont))
    if await procmsg(message,"py.ping"):
        await message.channel.send(content="Pong!")
    if await procmsg(message,"py.pong"):
        await message.channel.send(content="Ping!")
    if await procmsg(message,["hi","hello","hey"],nopfx=True):
        await message.channel.send(content="Greetings!")
    if await procmsg(message,["all.stop","py.stop","all.close","py.close","all.exit","py.exit","all.logout","py.logout","all.end","py.end","all.kill","py.kill"],reqop=True):
        await message.channel.send(content="Goodbye!")
        await client.close()
    if await procmsg(message,["all.token","py.token"],reqop=True):
        print(f"{message.author}<@!{message.author.id}> requested this bot's token and it was sent to them")
        await message.author.send(content=f"Here is the token you requested!\n```\n{token}\n```")
        await message.channel.send(content=":white_check_mark: Check your DMs! :white_check_mark:")
    elif await procmsg(message,["all.token","py.token"],reqop=False):
        print(f"{message.author}<@!{message.author.id}> requested this bot's token and it was not sent to them because they did not have the required permission")
        await message.channel.send(content=":x: You don't have the required permission. This incident has been logged. :x:")
    elif message.content=="all.lat":
        message.content="py.lat"
    elif message.content=="all.tst":
        message.content="py.tst"
    await client.process_commands(message)
@client.command()
async def tst(ctx):
    await ctx.send(content="I'm up!")
@client.command()
async def lat(ctx):
    l=int(client.latency*1000)
    await ctx.send(content=f"```\nDiscord.py Latency Now:      {l} ms\nDiscord.py Latency On Boot:  {startlat} ms\n```")
client.add_cog(jishaku.cog.Jishaku(bot=client))
client.run(token)
