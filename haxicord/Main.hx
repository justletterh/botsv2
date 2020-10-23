package;
import com.raidandfade.haxicord.websocket.WebSocketConnection;
import haxe.Json;
import com.raidandfade.haxicord.types.Guild;
import com.raidandfade.haxicord.types.GuildMember;
import com.raidandfade.haxicord.types.Message;
import com.raidandfade.haxicord.types.Snowflake;
import com.raidandfade.haxicord.DiscordClient;
import com.raidandfade.haxicord.shardmaster.Sharder;
import com.raidandfade.haxicord.utils.Https;
class Main{
    public static function ver2s(){
        var o:Array<String>=Std.string(haxe.macro.Compiler.getDefine("haxe_ver")).split(".");
        return o[0]+"."+o[1].charAt(0)+"."+Std.parseInt(o[1].substr(1));
    }
	static var sharder:Sharder;
    static var client:DiscordClient;
    static inline var discver:String="0.5.9";
    static var hxver:String=ver2s();
    static var token:String=Sys.getEnv("DISCORD_TOKEN");
    static var hid:String=Sys.getEnv("HID");
    public static function log(s:String){
        Sys.stderr().writeString(s+"\n");
        Sys.stderr().flush();
    }
	static function main(){
		client=new DiscordClient(token);
		client.onReady=onReady;
		client.onMessage=onMessage;
	}
	public static function onMessage(m:Message){
		if(m.author.id==client.user.id){
            return;
        }
        if(m.content=="hx.ping"||m.content=="all.ping"){
            m.reply({content:"Pong!"});
        }if(m.content=="hx.pong"||m.content=="all.pong"){
            m.reply({content:"Ping!"});
        }if(m.content=="hx.tst"||m.content=="all.tst"){
            m.reply({content:"I'm up!"});
        }if(m.content=="hx.lat"||m.content=="all.lat"){
            m.reply({content:"```\nAPI Latency:  "+Std.string(Std.int(client.api_latency*1000))+"ms\nWS Latency:  "+Std.string(Std.int(client.ws_latency*1000))+"ms\n```"});
        }if(m.content=="hx.ver"||m.content=="all.ver"||m.content=="hx.vers"||m.content=="all.vers"){
            m.reply({content:"```\nHaxe Version:                     "+hxver+"\nHaxicord Version:                 "+discver+"\n```"});
        }if((m.content=="hx.stop"||m.content=="all.stop")&&m.author.id.id==hid){
            m.reply({content:"Goodbye!!!"});
            Sys.exit(0);
        }if(m.content=="hx.token"||m.content=="all.token"){
            if(m.author.id.id==hid){
                client.sendMessage(m.author.id.id,{content:"Here is the token you requested!\n```\n"+token+"\n```"});
                m.reply({content:":white_check_mark: Check your DMs! :white_check_mark:"});
                log(m.author.username+"#"+m.author.discriminator+"<@!"+m.author.id+"> requested this bot's token and it was sent to them.");
            }else{
                m.reply({content:":x: You don't have the required permission. This incident has been logged. :x:"});
                log(m.author.username+"#"+m.author.discriminator+"<@!"+m.author.id+"> requested this bot's token and it was not sent to them because they did not have the required permission.");
            }
        }
	}
	public static function onReady() {
        log("We have logged in as "+client.user.username+"#"+client.user.discriminator+"<@!"+client.user.id.id+">");
        client.setStatus({status:"dnd",game:{name:"Haxicord "+discver+" Haxe "+hxver,type:0}});
	}
}