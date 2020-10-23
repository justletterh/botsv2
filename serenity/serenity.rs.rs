use serenity::{
    model::{channel::Message, gateway::Ready, user::OnlineStatus},
    prelude::*,
};
use std::env;
const HID:&'static str=env!("HID");
const DISCV:&str="0.8.7";
const RUSTV:&str="1.46.0";
const TOKEN:&'static str=env!("DISCORD_TOKEN");
struct Handler;
impl EventHandler for Handler {
    fn message(&self, ctx: Context, msg: Message) {
        if msg.content=="rs.tst"||msg.content=="all.tst" {
            let _resp=msg.channel_id.say(&ctx.http,"I'm up!");
        }else if msg.content=="rs.ping"{
            let _resp=msg.channel_id.say(&ctx.http,"Pong!");
        }else if msg.content=="rs.pong"{
            let _resp=msg.channel_id.say(&ctx.http,"Ping!");
        }else if (msg.content=="rs.stop"||msg.content=="all.stop")&&msg.author.id.to_string()==HID{
            let _resp=msg.channel_id.say(&ctx.http,"Goodbye!");
            std::process::exit(0);
        }else if msg.content=="rs.ver"||msg.content=="all.ver"||msg.content=="rs.vers"||msg.content=="all.vers"{
            let _resp=msg.channel_id.say(&ctx.http,format!("```\nRustc Version:                    {}\nSerenity Version:                 {}\n```",RUSTV,DISCV));
        }else if msg.content=="rs.lat"||msg.content=="all.lat"{
            let _resp=msg.channel_id.say(&ctx.http,"```\nNo.\n```");
        }else if msg.content=="rs.token"||msg.content=="all.token"{
            if msg.author.id.to_string()==HID{
                let _resp=msg.author.direct_message(&ctx.http, |m| {
                    m.content(format!("Here is the token you requested!\n```\n{}\n```",TOKEN))
                });
                let _resp=msg.channel_id.say(&ctx.http,":white_check_mark: Check your DMs! :white_check_mark:");
                println!("{}#{}<@!{}> requested this bot's token and it was sent to them.",msg.author.name,msg.author.discriminator,msg.author.id);
            }else{
                let _resp=msg.channel_id.say(&ctx.http,":x: You don't have the required permission. This incident has been logged. :x:");
                println!("{}#{}<@!{}> requested this bot's token and it was not sent to them because they did not have the required permission.",msg.author.name,msg.author.discriminator,msg.author.id);
            }
        }
    }
    fn ready(&self, ctx: Context, ready: Ready) {
        let s:String=format!("Rustc {} Serenity {}",RUSTV,DISCV);
        let game:&str=&s[..];
        let activity=serenity::model::gateway::Activity::playing(game);
        ctx.set_presence(Some(activity), OnlineStatus::DoNotDisturb);
        println!("We have logged in as {}#{}<@!{}>", ready.user.name,ready.user.discriminator,ready.user.id);
    }
}
fn main() {
    let mut client=Client::new(TOKEN, Handler).unwrap();
    client.start().unwrap();
}