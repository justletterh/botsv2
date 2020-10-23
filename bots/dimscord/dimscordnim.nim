import dimscord, asyncdispatch, times, options, os, system
let
    token=getEnv("DISCORD_TOKEN")
    discord=newDiscordClient(token)
    hid=getEnv("HID")
    nimv=NimVersion
    discv=dimscord.libVer
discord.events.on_ready = proc (s: Shard, r: Ready) {.async.} =
    echo "We have logged in as " & $r.user & "<@!" & $r.user.id & ">"
    await s.updateStatus(game = some GameStatus(name: "Nim " & $nimv & " Dimscord " & discv,kind: gatPlaying), status = "dnd")
discord.events.message_create = proc (s: Shard, m: Message) {.async.} =
    if m.author.id=="758547806129487914": return
    if m.content=="nim.lat" or m.content=="all.lat":
        let
            before = epochTime() * 1000
            msg = await discord.api.sendMessage(m.channel_id, "```\nloading...\n```")
            after = epochTime() * 1000
        discard await discord.api.editMessage(m.channel_id, msg.id, "```\nThis bot took " & $int(after - before) & " ms to edit this message\nLatency is " & $s.latency() & " ms now\n```")
    elif m.content=="nim.tst" or m.content=="all.tst":
        discard await discord.api.sendMessage(m.channel_id, "I'm up!")
    elif m.content=="nim.pong":
        discard await discord.api.sendMessage(m.channel_id, "Ping!")
    elif m.content=="nim.ping":
        discard await discord.api.sendMessage(m.channel_id, "Pong!")
    elif (m.content=="nim.close" or m.content=="all.close" or m.content=="all.stop" or m.content=="nim.stop") and m.author.id==hid:
        discard await discord.api.sendMessage(m.channel_id, "Goodbye!")
        quit(0)
    elif m.content=="nim.ver" or m.content=="nim.vers" or m.content=="nim.version" or m.content=="all.ver" or m.content=="all.vers" or m.content=="all.version":
        discard await discord.api.sendMessage(m.channel_id, "```\nDimscord Version:                 " & $discv & "\nNim Version:                      " & $nimv & "\n```")
    elif m.content=="all.token" or m.content=="nim.token":
        if m.author.id==hid:
            echo $m.author & "<@!" & $m.author.id & "> requested this bot's token and it was sent to them"
            discard await discord.api.sendMessage(m.channel_id,":white_check_mark: Check your DMs! :white_check_mark:")
            let dm=await discord.api.createUserDm(m.author.id)
            discard await discord.api.sendMessage(dm.id,"Here is the token you requested!\n```\n" & $token & "\n```")
        else:
            echo $m.author & "<@!" & $m.author.id & "> requested this bot's token and it was not sent to them because they did not have the required permission"
            discard await discord.api.sendMessage(m.channel_id,":x: You don't have the required permission. This incident has been logged. :x:")
waitFor discord.startSession()