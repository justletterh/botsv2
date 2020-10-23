import discord,time,datetime,uuid,psutil,os,asyncio
from asyncio import sleep
from cpuinfo import get_cpu_info as cpuinf
token=os.getenv("DISCORD_TOKEN")
hid=os.environ['HID']
appid=763784214259957811
count=0
delay=15
pfx="1."
client1=discord.Client()
client2=discord.Client()
class Color:
    def __repr__(self):
        return self.id
    def __init__(self,id,txt=""):
        self.id=str(id)
        self.txt=txt
green=Color(764285719396220958,"Ideal")
yellow=Color(764285719333044254,"Operational")
orange=Color(764285719266721802,"Severe")
red=Color(764285719207477259,"Critical")
def level(x):
    if 25>=x:
        return globals()['green']
    elif 50>=x:
        return globals()['yellow']
    elif 85>=x:
        return globals()['orange']
    else:
        return globals()['red']
def splitstr(s):
    o=[]
    for c in s:
        o.append(c)
    return o
def clean(n):
    return str(round(n))
def cleanfreq(n):
    n=splitstr(clean(n))
    n[1]=f".{n[1]}"
    return float("".join(n))
def tstamp():
    epoch=datetime.datetime.fromtimestamp(0)
    now=datetime.datetime.now()
    if now.day==1 and now.month==1:
        now=now.replace(year=now.year-1,month=12,day=mr(now.year-1,12)[1])
    elif now.day!=1:
        now=now.replace(day=now.day-1)
    else:
        now=now.replace(month=now.month-1,day=mr(now.year,now.month-1)[1])
    return ((now-epoch).total_seconds())+15
def sig(msg,s,*,indent=4):
    return f"\u17b5\n{msg}\n{' '*indent}{s}"
def proc(msg,cmd,*,epfx=[],arg=None,nodef=False):
    l=epfx
    if type(l)!=list:
        l=[l.lower()]
    else:
        tmp=[]
        for i in l:
            tmp.append(i.lower())
        l=tmp
    if not nodef:
        try:
            l.append(globals()['pfx'].lower())
        except KeyError:
            pass
    msg=msg.lower()
    ret=False
    for i in l:
        if f"{i}{cmd}" in msg:
            ret=True
    if ret:
        if " " in msg and arg!=None:
            args=msg.split(" ")
            tmp=[]
            for a in args:
                tmp.append(a.lower())
            if args[1]!=arg:
                ret=False
        elif arg!=None:
            ret=False
    return ret
async def update():
    cstatus="CPU Metrics"
    status="dnd"
    emoji_name="\U0001f4c8"
    emoji_id=None
    await client1.change_presence(activity=discord.Activity(state=cstatus,details=" ",name=" ",emoji={'name':emoji_name,'id':emoji_id},type=discord.ActivityType.custom),status="dnd")
    await sleep(delay*2)
async def update_loop():
    while True:
        percnt=psutil.cpu_percent()
        si=level(percnt)
        name=f"{cpuinf()['brand_raw']} {cpuinf()['arch']}"
        details=f"CPU Percent: {clean(percnt)}%"
        limg="764294359675043900"
        ltxt="CPU Metrics"
        simg=si.id
        stxt=si.txt
        pmin=os.getpid()
        pmax=max(psutil.pids())
        atype=discord.ActivityType.playing
        status="dnd"
        state=f"CPU Frequency: {cleanfreq(psutil.cpu_freq().current)}GHz | PID: "
        stamp=tstamp()
        await client2.change_presence(activity=discord.Activity(application_id=appid,name=name,state=state,details=details,assets={"large_image":limg,"large_text":ltxt,"small_image":simg,"small_text":stxt},party={"id":str(uuid.uuid4()), "size":[pmin,pmax]},timestamps={"start":stamp},type=atype), status=status)
        await sleep(delay)
@client1.event
async def on_ready():
    print(f"We have logged in as {client1.user}<@!{client1.user.id}> -Status")
    while True:
        await update()
@client1.event
async def on_message(message):
    arg="status"
    if message.author.id==hid:
        if proc(message.content,"stop",arg=arg):
            await message.channel.send(content="Goodbye!")
            await client1.close()
        if proc(message.content,"stop",epfx="all.",nodef=True) or proc(message.content,"stop") and (f" {arg}" not in message.content and " game" not in message.content):
            await message.channel.send(content=sig("Goodbye!","-*Status*"))
            await client1.close()
        if proc(message.content,"tst",arg=arg):
            await message.channel.send(content="I'm up!")
        if proc(message.content,"tst",epfx="all.",nodef=True) or proc(message.content,"tst") and (f" {arg}" not in message.content and " game" not in message.content):
            await message.channel.send(content=sig("I'm up!","-*Status*"))
@client2.event
async def on_ready():
    print(f"We have logged in as {client2.user}<@!{client2.user.id}> -Game")
    await update_loop()
@client2.event
async def on_message(message):
    arg="game"
    if message.author.id==hid:
        if proc(message.content,"stop",arg=arg):
            await message.channel.send(content="Goodbye!")
            await client2.close()
        if proc(message.content,"stop",epfx="all.",nodef=True) or proc(message.content,"stop") and (f" {arg}" not in message.content and " status" not in message.content):
            await message.channel.send(content=sig("Goodbye!","-*Game*"))
            await client2.close()
        if proc(message.content,"tst",arg=arg):
            await message.channel.send(content="I'm up!")
        if proc(message.content,"tst",epfx="all.",nodef=True) or proc(message.content,"tst") and (f" {arg}" not in message.content and " status" not in message.content):
            await message.channel.send(content=sig("I'm up!","-*Game*"))
loop=asyncio.get_event_loop()
loop.create_task(client1.start(token,bot=False))
loop.create_task(client2.start(token,bot=False))
loop.run_forever()