from sys import argv as args
from time import sleep
import discord
from discord.ext import commands
def main(t):
    hid=666317117154525185
    async def is_owner(ctx):
        return ctx.author.id==hid
    client=commands.Bot(command_prefix="other.",case_insensitive=True)
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
            await client.stop()
        if message.content.lower().startswith("all.tst"):
            await message.channel.send(content="I'm up!")
        await client.process_commands(message)
    @client.event
    async def on_ready():
        startlat=int(client.latency*1000)
        print(f"We have logged in as {client.user}<@!{client.user.id}> With a Starting Latency of {startlat} ms")
        await client.change_presence(status="dnd",activity=discord.Game(f"{startlat} ms On Boot"))
    client.run(t)
class ArgError(Exception):
    pass
try:
    run=True
    token=args[1]
except IndexError:
    run=False
    token=None
if run:
    main(token)
else:
    #this is only called if no argument is passed
    raise ArgError("A Token Was Not Given in the Command-Line Arguments")