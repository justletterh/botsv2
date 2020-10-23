using Discord,Logging,Dates
import Pkg
discv=string(Pkg.installed()["Discord"])
jlv=VERSION
token=ENV["DISCORD_TOKEN"]
cl=Client(token; presence=(game=(name=string("Julia $(jlv) Discord.jl $(discv)"), type=AT_GAME),status="dnd"),prefix="jl.")
hid=convert(UInt64,parse(Int,ENV["HID"]))
module Sandbox end
function codeblock(val)
s = val === nothing ? "nothing" : string(val)
return "```julia\n$s\n```"
end
function parsecode(code::AbstractString)
return try
Meta.parse("begin $code end")
catch e
:(sprint(showerror, $e))
end
end
function eval_codeblock(c::Client, msg::Message, code::Expr)
if msg.author.id!=hid
return
end
result = try
@eval Sandbox $code
catch e
sprint(showerror, e)
end
reply(c, msg, codeblock(result))
end
function cmd(msg::Message,l::Array{String},op::Bool=false)
if op && msg.author.id!=hid
return false
end
for pfx in l
if occursin(pfx,lowercase(msg.content))
return true
end
end
return false
end
function log(s)
write(stdout,string(s,"\n"))
flush(stdout)
end
function msghandler(cl::Client, e::MessageCreate)
heartbeat_ping(cl)
if e.message.author.id==me(cl).id
return
end
if cmd(e.message,["all.tst","jl.tst"])
reply(cl,e.message,"I'm up!")
end
if cmd(e.message,["jl.ping"])
reply(cl,e.message,"Pong!")
end
if cmd(e.message,["jl.pong"])
reply(cl,e.message,"Ping!")
end
if cmd(e.message,["jl.stop","all.stop","jl.close"],true)
reply(cl,e.message,"Goodbye!")
close(cl)
end
if cmd(e.message,["jl.ver","jl.vers","all.ver","all.vers"])
reply(cl,e.message,"```\nJulia Version:                    $(jlv)\nDiscord.jl Version:               $(discv)\n```")
end
if cmd(e.message,["jl.lat","all.lat"])
global lat=heartbeat_ping(cl)
while lat==Nothing()
global lat=heartbeat_ping(cl)
end
global lat=string(Dates.value(lat))
global startlat
reply(cl,e.message,"```\nDiscord.jl Latency Now:      $(lat)\nDiscord.jl Latency On Boot:  $(startlat)\n```")
end
if cmd(e.message,["jl.token","all.token"],true)
reply(cl,e.message,":white_check_mark: Check your DMs! :white_check_mark:")
dm=fetchval(create_dm(cl;recipient_id=hid))
create(cl,Message,dm; content="Here is the token you requested!\n```\n$(token)\n```")
log("$(e.message.author.username)#$(e.message.author.discriminator)<@!$(e.message.author.id)> requested this bot's token and it was sent to them")
end
if cmd(e.message,["jl.token","all.token"],false)&&e.message.author.id!=hid
reply(cl,e.message,":x: You don't have the required permission. This incident has been logged. :x:")
log("$(e.message.author.username)#$(e.message.author.discriminator)<@!$(e.message.author.id)}> requested this bot's token and it was not sent to them because they did not have the required permission")
end
end
function readyhandler(cl::Client, e::Ready)
global startlat=heartbeat_ping(cl)
global tries=0
while startlat==Nothing()
global tries+=1
if tries==50
global startlat=Dates.Millisecond(50)
break
end
global startlat=heartbeat_ping(cl)
end
global startlat=string(Dates.value(startlat))
global clusr=me(cl)
log(string("We have logged in as ",clusr.username,"#",clusr.discriminator,"<@!",clusr.id,">"))
end
add_command!(cl, :eval, eval_codeblock;parsers=[parsecode], pattern=r"^eval ```(?:julia)?\n(.*)\n```")
add_handler!(cl,MessageCreate,msghandler)
add_handler!(cl,Ready,readyhandler)
open(cl)
wait(cl)