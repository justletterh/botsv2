package main
import (
    "fmt"
    "os"
    "log"
    "os/exec"
    "os/signal"
    "syscall"
    "github.com/bwmarrin/discordgo"
    "strings"
    "time"
)
var hid=os.Getenv("HID")
var token=os.Getenv("DISCORD_TOKEN")
const startlat="50"
func anyin(s string, l []string) bool {
    for i := 0; i < len(l); i++ {
        if strings.Contains(s,l[i]){
            return true
        }
    }
    return false
}
func get_gover()string{
    out,err:=exec.Command("/bin/bash","-c","echo `go version|{ read _ _ v _; echo ${v#go};}`").Output()
    if err != nil {
        log.Fatal(err)
    }
    out=[]byte(strings.ReplaceAll(fmt.Sprintf("%s",out),"\n",""))
    return fmt.Sprintf("%s",out)
}
func main() {
	dg, err := discordgo.New(fmt.Sprintf("Bot %s",token))
	if err != nil {
		fmt.Println("error creating Discord session,", err)
		return
	}
    dg.AddHandler(ready)
	dg.AddHandler(messageCreate)
	dg.Identify.Intents = discordgo.MakeIntent(discordgo.IntentsGuildMessages)
	err = dg.Open()
	if err != nil {
		fmt.Println("error opening connection,", err)
		return
	}
	sc := make(chan os.Signal, 1)
	signal.Notify(sc, syscall.SIGINT, syscall.SIGTERM, os.Interrupt, os.Kill)
	<-sc
	dg.Close()
}
func ready(s *discordgo.Session, event *discordgo.Ready) {
    g:=discordgo.Game {Name: fmt.Sprintf("GoLang %s DiscordGo %v",get_gover(),discordgo.VERSION), Type: discordgo.GameTypeGame}
    usd := discordgo.UpdateStatusData{AFK: false, Status: "dnd",Game:&g}
	s.UpdateStatusComplex(usd)
    fmt.Printf("We have logged in as %s#%s<@!%s>\n",s.State.User.Username,s.State.User.Discriminator,s.State.User.ID)
}
func messageCreate(s *discordgo.Session, m *discordgo.MessageCreate) {
	if m.Author.ID == s.State.User.ID {
		return
	}
	if m.Content=="go.ping"{
		s.ChannelMessageSend(m.ChannelID,"Pong!")
	}
	if m.Content=="go.pong"{
		s.ChannelMessageSend(m.ChannelID,"Ping!")
	}
	if anyin(m.Content,[]string {"all.version","go.version","go.ver","all.ver"}){
		s.ChannelMessageSend(m.ChannelID,fmt.Sprintf("```\nGolang Version:                   %s\nDiscordgo Version:                %v\n```",get_gover(),discordgo.VERSION))
	}
    if anyin(m.Content,[]string {"all.stop","go.stop","all.close","go.close","all.kill","go.kill"})==true&&m.Author.ID==hid{
        s.ChannelMessageSend(m.ChannelID,"Goodbye!")
        err:=s.Close()
        if err != nil {
            log.Fatal(err)
        }
        syscall.Kill(syscall.Getpid(), syscall.SIGINT)
    }
    if anyin(m.Content,[]string {"all.token","go.token"})==true&&m.Author.ID==hid{
        dm,err:=s.UserChannelCreate(m.Author.ID)
        if err != nil {
            log.Fatal(err)
        }
        s.ChannelMessageSend(dm.ID,fmt.Sprintf("Here is the token you requested!\n```\n%s\n```",token))
        s.ChannelMessageSend(m.ChannelID,":white_check_mark: Check your DMs! :white_check_mark:")
        fmt.Printf("%s#%s<@!%s> requested this bot's token and it was sent to them.\n",m.Author.Username,m.Author.Discriminator,m.Author.ID)
    }
    if anyin(m.Content,[]string {"all.token","go.token"})==true&&m.Author.ID!=hid{
        s.ChannelMessageSend(m.ChannelID,":x: You don't have the required permission. This incident has been logged. :x:")
        fmt.Printf("%s#%s<@!%s> requested this bot's token and it was not sent to them because they did not have the required permission.\n",m.Author.Username,m.Author.Discriminator,m.Author.ID)
    }
    if anyin(m.Content,[]string {"all.tst","go.tst"}){
        s.ChannelMessageSend(m.ChannelID,"I'm up!")
    }
    if anyin(m.Content,[]string {"all.lat","go.lat"}){
        s.ChannelMessageSend(m.ChannelID,strings.ReplaceAll(fmt.Sprintf("```\nDiscordGo Latency on Boot:   %s ms\nDiscordGo Latency Now:       %v\n```",startlat,s.HeartbeatLatency().Round(time.Millisecond)),"ms"," ms"))
    }
}