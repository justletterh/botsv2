import discord,platform,os
from discord.ext import commands
t=os.environ['DISCORD_TOKEN']
pfx=os.environ['DISCORD_PFX']
hid=int(os.environ['HID'])
async def is_owner(ctx):
    return ctx.author.id==hid
client=commands.Bot(command_prefix=pfx,case_insensitive=True)
@client.command()
async def tst(ctx):
    await ctx.send(content="I'm up!")
@client.command()
@commands.check(is_owner)
async def stop(ctx):
    await ctx.send(content="Goodbye!")
    await client.close()
@client.event
async def on_message(message):
    op=await is_owner(message)
    if message.author.id==client.user.id:
        return
    if message.content.lower().startswith("all.stop") and op:
        await message.channel.send(content="Goodbye!")
        await client.close()
    if message.content.lower().startswith("all.tst"):
        await message.channel.send(content="I'm up!")
    if message.content.lower().startswith(f"{pfx}token") or message.content.lower().startswith("all.token"):
        if op:
            print(f"{message.author}<{message.author.id}> requested this bot's token and it was sent to them")
            await message.author.send(content=f"Here is the token you requested!\n```\n{t}\n```")
            await message.channel.send(content=":white_check_mark: Check your DMs! :white_check_mark:")
        elif not op:
            print(f"{message.author}<{message.author.id}> requested this bot's token and it was not sent to them because they did not have the required permission")
            await message.channel.send(content=":x: You don't have the required permission. This incident has been logged. :x:")
    await client.process_commands(message)
@client.event
async def on_ready():
    startlat=int(client.latency*1000)
    pyver=platform.python_version()
    discver=discord.__version__
    print(f"We have logged in as {client.user}<@!{client.user.id}>")
    await client.change_presence(status="dnd",activity=discord.Game(f"Python {pyver} Discord.py {discver}"))
@client.event
async def on_command_error(ctx, error):
    if isinstance(error,commands.errors.CommandNotFound):
        pass
client.run(t)