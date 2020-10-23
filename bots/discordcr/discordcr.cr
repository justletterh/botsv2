require "../deps/src/discordcr"
require "io"
token=sprintf("Bot %s",ENV["DISCORD_TOKEN"])
botid=UInt64.new(ENV["DISCORD_ID"])
discv="0.4.0"
client = Discord::Client.new(token: token, client_id: botid)
cache = Discord::Cache.new(client)
client.cache = cache
io=IO::Memory.new
Process.run("crystal --version", shell: true, output: io)
crv=io.to_s.split("\n")[0].sub("Crystal ","").split(" ")[0]
hid=UInt64.new(ENV["HID"])
def cmd(s,pfx)
pfx.each do |i|
if s.starts_with? i
return true
end
end
return false
end
client.on_ready do |payload|
c=cache.resolve_user(botid)
puts "We have logged in as #{c.username}##{c.discriminator}<@!#{c.id}>"
client.status_update("dnd",game:Discord::GamePlaying.new(name:"Crystal #{crv} Discordcr #{discv}",type:Discord::GamePlaying::Type::Playing))
end
client.on_message_create do |payload|
if payload.author.id.value!=botid
cont=payload.content
if cmd(cont,["cr.lat","all.lat"])
m = client.create_message(payload.channel_id, "```\nloading...\n```")
time = Time.utc - payload.timestamp
lat="#{time.total_milliseconds.round()}".sub(".0","")
client.edit_message(m.channel_id, m.id, "```\nit took this bot #{lat} ms to edit this message.\n```")
end
if cmd(cont,["cr.tst","all.tst"])
client.create_message(payload.channel_id,"I'm up!")
end
if cmd(cont,["cr.ver","cr.vers","all.ver","all.vers"])
client.create_message(payload.channel_id,"```\nCrystal Version:                  #{crv}\nDiscordcr Version:                #{discv}\n```")
end
if payload.author.id==hid
if cmd(cont,["all.stop","cr.stop"])
client.create_message(payload.channel_id,"Goodbye!")
client.stop()
end
end
if cmd(cont,["cr.ping"])
client.create_message(payload.channel_id,"Pong!")
client.stop()
end
if cmd(cont,["cr.pong"])
client.create_message(payload.channel_id,"Ping!")
client.stop()
end
if cmd(cont,["all.token","cr.token"])
if payload.author.id==hid
puts "#{payload.author.username}##{payload.author.discriminator}<@!#{payload.author.id}> requested this bot's token and it was sent to them."
client.create_message(payload.channel_id,":white_check_mark: Check your DMs! :white_check_mark:")
client.create_message(client.create_dm(payload.author.id).id,"Here is the token you requested!\n```#{token.sub("Bot ","")}\n```")
else
puts "#{payload.author.username}##{payload.author.discriminator}<@!#{payload.author.id}> requested this bot's token and it was not sent to them because they did not have the required permission."
client.create_message(payload.channel_id,":x: You don't have the required permission. This incident has been logged. :x:")
end
end
end
end
client.run