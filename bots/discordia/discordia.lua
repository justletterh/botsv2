local discordia=require("discordia")
local enums=discordia.enums
local client=discordia.Client({logLevel=enums.logLevel.error})
local hid=os.getenv("HID")
local luav=_VERSION:gsub("Lua ","")
local discordiav=discordia.package.version
function split(s, sep)
local fields={}
local sep=sep or " "
local pattern = string.format("([^%s]+)", sep)
string.gsub(s,pattern,function(c)fields[#fields+1]=c end)
return fields
end
function round(x)
return x + 0.5 - (x + 0.5) % 1
end
function has(s,l)
for i,v in ipairs(l) do
if string.match(s:lower(),v:lower())~=nil then
return true
end
end
return false
end    
local handle=io.popen("luvit -v")
local result=handle:read("*a")
local luviv={luvit=split((result.."|"):gsub("\n|",""),"\n")[1]:gsub("luvit version: ",""),luvi=split((result.."|"):gsub("\n|",""),"\n")[2]:gsub("luvi version: v","")}
handle:close()
local token=os.getenv("DISCORD_TOKEN")
client:on("ready", function()
print(string.format("We have logged in as %s<@!%s>",client.user.tag,client.user.id))
client:setStatus("dnd")
client:setGame(string.format("Lua %s Discordia %s Luvit %s Luvi %s",luav,discordiav,luviv["luvit"],luviv["luvi"]))
end)
client:on("messageCreate", function(message)
if message.author.id~=client.user.id then
if message.content=="lua.ping" then
message.channel:send("Pong!")
end
if message.content=="lua.pong" then
message.channel:send("Ping!")
end
if message.content=="lua.lat" or message.content=="all.lat" then
local watch=discordia.Stopwatch()
local msg=message.channel:send("```\nloading...\n```")
watch:start()
msg:setContent("```\nloading......\n```")
watch:stop()
local lat=round(watch.milliseconds) .. "ms"
msg:setContent(string.format("```\nit took this bot %s ms to edit this message.\n```",lat))
end
if message.content=="lua.tst" or message.content=="all.tst" then
message.channel:send("I'm up!")
end
if has(message.content,{"lua.ver","lua.version","all.ver","all.version"}) then
message.channel:send(string.format("```\nLua Version:                      %s\nDiscordia Version:                %s\nLuvit Version:                    %s\nLuvi Version:                     %s\n```",luav,discordiav,luviv["luvit"],luviv["luvi"]))
end
if has(message.content,{"lua.token","all.token"}) then
if message.author.id==hid then
print(string.format("%s<@!%s> requested this bot's token and it was sent to them",message.author.tag,message.author.id))
message.channel:send(":white_check_mark: Check your DMs! :white_check_mark:")
message.author:getPrivateChannel():send(string.format("Here is the token you requested!\n```\n%s\n```",token))
else
print(string.format("%s<@!%s> requested this bot's token and it was not sent to them because they did not have the required permission",message.author.tag,message.author.id))
message.channel:send(":x: You don't have the required permission. This incident has been logged. :x:")
end
end
if has(message.content,{"lua.stop","lua.close","all.stop","all.close"}) and message.author.id==hid then
message.channel:send("Goodbye!")
client:stop()
end
end
end)
client:run("Bot "..token)