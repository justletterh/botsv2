import discord,jishaku,platform,os
from discord.ext import commands
from json import loads as jload
cmdpfx="util."
cpfx=cmdpfx
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
async def etest(m):
    e=discord.Embed(title="Title",description='Description')
    e.set_thumbnail(url=client.user.avatar_url)
    e.set_footer(text='Footer', icon_url=client.get_user(hid).avatar_url)
    e.add_field(name='Field 1 Title',value='Field 1 Value',inline=True)
    e.add_field(name='Field 2 Title',value='Field 2 Value',inline=True)
    e.add_field(name='Field 3 Title',value='Field 3 Value',inline=True)
    e.add_field(name='Field 4 Title',value='Field 4 Value',inline=True)
    e.add_field(name='Field 5 Title',value='Field 5 Value',inline=True)
    e.add_field(name='Field 6 Title',value='Field 6 Value',inline=True)
    e.add_field(name='Field 7 Title',value='Field 7 Value',inline=True)
    e.add_field(name='Field 8 Title',value='Field 8 Value',inline=True)
    e.add_field(name='Field 9 Title',value='Field 9 Value',inline=True)
    await m.channel.send(content="Content",embed=e)
async def botrole(m):
    if await is_owner(m) or override:
        args=" ".join(m.content.split(" ")[1:len(m.content.split(" "))])
        args=args.split(" --ids ")
        roles=args[0].split(" ")
        o=[]
        for r in roles:
            o.append(m.guild.get_role(int(r)))
        roles=o
        users=args[1].split(" ")
        o=[]
        for u in users:
            o.append(m.guild.get_member(int(u)))
        users=o
        for mem in users:
            await mem.add_roles(*roles)
        await m.channel.send(content="Done!!!")
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
    if await procmsg(message,[f"{cpfx}ver","all.ver",f"{cpfx}version","all.version",f"{cpfx}vers","all.vers"],reqop=False):
        cont=["```"]
        for v in vers:
            cont.append(f"{v} Version:{(25-len(v))*' '}{vers[v]}")
        cont.append("```")
        await message.channel.send(content="\n".join(cont))
    if await procmsg(message,f"{cpfx}ping"):
        await message.channel.send(content="Pong!")
    if await procmsg(message,f"{cpfx}pong"):
        await message.channel.send(content="Ping!")
    if await procmsg(message,["hi","hello","hey"],nopfx=True):
        await message.channel.send(content="Greetings!")
    if await procmsg(message,["all.stop",f"{cpfx}stop","all.close",f"{cpfx}close","all.exit",f"{cpfx}exit","all.logout",f"{cpfx}logout","all.end",f"{cpfx}end","all.kill",f"{cpfx}kill"],reqop=True):
        await message.channel.send(content="Goodbye!")
        await client.close()
    if await procmsg(message,["all.token",f"{cpfx}token"],reqop=True):
        print(f"{message.author}<@!{message.author.id}> requested this bot's token and it was sent to them")
        await message.author.send(content=f"Here is the token you requested!\n```\n{token}\n```")
        await message.channel.send(content=":white_check_mark: Check your DMs! :white_check_mark:")
    elif await procmsg(message,["all.token",f"{cpfx}token"],reqop=False):
        print(f"{message.author}<@!{message.author.id}> requested this bot's token and it was not sent to them because they did not have the required permission")
        await message.channel.send(content=":x: You don't have the required permission. This incident has been logged. :x:")
    elif message.content=="all.lat":
        message.content=f"{cpfx}lat"
    elif message.content=="all.tst":
        message.content=f"{cpfx}tst"
    elif message.content.startswith("all.embed"):
        await etest(message)
    elif message.content.startswith("all.role") or message.content.startswith("util.role"):
        await botrole(message)
    await client.process_commands(message)
@client.command()
async def tst(ctx):
    await ctx.send(content="I'm up!")
@client.command()
async def embed(ctx):
    await etest(ctx)
@client.command()
async def lat(ctx):
    l=int(client.latency*1000)
    await ctx.send(content=f"```\nDiscord.py Latency Now:      {l} ms\nDiscord.py Latency On Boot:  {startlat} ms\n```")
client.add_cog(jishaku.cog.Jishaku(bot=client))
client.run(token)
