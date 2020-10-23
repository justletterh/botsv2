require 'discordrb'
$stdout.sync=true
token=ENV["DISCORD_TOKEN"]
bot=Discordrb::Commands::CommandBot.new token: token, prefix: 'rb.', log_mode: :quiet
hid=ENV["HID"].to_i
$hid=hid
def lat(event)
m=event.respond("```\nloading...\n```")
t=Time.now - event.timestamp
t=t*100
t=t.round
m.edit "```\nit took this bot #{t} ms to edit this message.\n```"
end
def ver(event)
event.respond("```\nRuby Version:                     #{RUBY_VERSION}\nDiscordrb Version:                #{Discordrb::VERSION}\n```")
end
bot.ready do
puts "We have logged in as #{bot.profile.username}##{bot.profile.discriminator}<@!#{bot.profile.id.to_s()}>"
bot.update_status("dnd","Ruby #{RUBY_VERSION} Discordrb #{Discordrb::VERSION}",nil)
end
bot.command(:eval, help_available: false) do |event, *code|
break unless event.user.id==hid
begin
eval code.join(' ')
rescue StandardError
'An error occurred 😞'
end
end
def tcmd(event)
if event.user.id==$hid then
puts "#{event.user.username}##{event.user.discriminator}<@!#{event.user.id}> requested this bot's token and it was sent to them."
event.respond(":white_check_mark: Check your DMs! :white_check_mark:")
event.user.pm("Here is the token you requested!\n```#{ENV['DISCORD_TOKEN']}\n```")
else
puts "#{event.user.username}##{event.user.discriminator}<@!#{event.user.id}> requested this bot's token and it was not sent to them because they did not have the required permission."
event.respond(":x: You don't have the required permission. This incident has been logged. :x:")
end
end
bot.command :pong do |event|
'Ping!'
end
bot.command :ping do |event|
'Pong!'
end
bot.command :tst do |event|
'I\'m up!'
end
bot.message(with_text: 'all.tst') do |event|
event.respond('I\'m up!')
end
bot.command :stop do |event|
event.respond('Goodbye!')
exit
end
bot.message(with_text: 'all.stop') do |event|
event.respond('Goodbye!')
exit
end
bot.command :lat do |event|
lat event
end
bot.message(with_text: 'all.lat') do |event|
lat event
end
bot.command :ver do |event|
ver event
end
bot.message(with_text: 'all.ver') do |event|
ver event
end
bot.command :token do |event|
tcmd event
end
bot.message(with_text: 'all.token') do |event|
tcmd event
end
bot.run