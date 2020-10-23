const Eris=require("eris");
const Util=require("util");
const process=require("process");
const {execSync}=require('child_process');
const token=process.env.DISCORD_TOKEN;
var bot = new Eris(token);
var startlat;
const cmdpfx="eris.";
const hid=process.env.HID;
function replall(s,ss,sss=""){
    return s.replace(new RegExp(ss, "g"), sss);
}
function cmd(s){
    return replall(execSync(s,{ encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 }).toString(),"\n");
}
const nodever=cmd("node --version");
const erisver=cmd("npm info eris version");
function is_owner(msg){
    return msg.author.id==hid;
}
function cleanl(i,ii){
    var index;
    while(i.includes(ii)){
        index=i.indexOf(ii);
        if(index>-1){
            i.splice(index, 1);
        }}return i;
}
function anystart(l,s){
    for(i in l){
        i=l[i];
        if (i.startsWith(s)){
            return true;
        }}return false;
}
function procmsg(msg,pfx,reqop=false,nopfx=false){
    var tmp;
    if (typeof(pfx)==='string'){
        pfx=[pfx];
    }
    tmp=[];
    for (i in pfx){
        i=pfx[i];
        tmp.push(replall(i.toLowerCase())," ");
    }
    pfx=cleanl(tmp," ");
    if (nopfx){
        tmp=[];
        for (i in pfx){
            i=pfx[i];
            tmp.push(cmdpfx+i);
        }pfx=tmp;
    }if (reqop&&!is_owner(msg)){
        return false;
    }else if (anystart(pfx,msg.content.toLowerCase())){
        return true;
    }else {
        return false;
    }
}
async function evalcmd(code){
    code=code.replace("eris.eval ","");
    if (e = code.match(/^```js\n([^]*)\n```$/)) code = e[1];
    let out;
    try {
        code.split("\n").length > 1 ? (out = await eval(`(async () => {${code}})();`)) : (out = await eval(code));
    } catch(e) { out = e.toString(); }
    out = Util.inspect(out);
    out=out.slice(0,1990);
    return `\`\`\`\n${out}\n\`\`\``;
}
bot.on("ready",()=>{
    if (!startlat) startlat=bot.shards.get(0).latency;
    console.log(`We have logged in as ${bot.user.username}#${bot.user.discriminator}<@!${bot.user.id}>`);
    bot.editStatus("dnd",{name:`NodeJS ${nodever} Eris ${erisver}`});
});
bot.on("messageCreate",async(msg)=>{
    if(msg.author.id==bot.user.id){
        return 0;
    }else if(procmsg(msg,"eris.ping")){
        bot.createMessage(msg.channel.id, "Pong!");
    }else if(procmsg(msg,"eris.pong")){
        bot.createMessage(msg.channel.id, "Ping!");
    }else if(procmsg(msg,["eris.lat","all.lat"],false,false)){
        bot.createMessage(msg.channel.id,`\`\`\`\nEris Latency Now:      ${Util.inspect(bot.shards.get(0).latency)} ms\nEris Latency On Boot:  ${Util.inspect(startlat)} ms\n\`\`\``);
    }else if(procmsg(msg,["eris.token","all.token"],true,false)){
        console.log(`${msg.author.username}@${msg.author.discriminator}<${msg.author.id}> requested this bot's token and it was sent to them.`);
        bot.createMessage(msg.channel.id,":white_check_mark: Check your DMs! :white_check_mark:");
        bot.getDMChannel(msg.author.id).then(dm => dm.createMessage(`Here is the token you requested!\n\`\`\`\n${token}\n\`\`\``));
    }else if(procmsg(msg,["eris.token","all.token"],false,false)){
        console.log(`${msg.author.username}@${msg.author.discriminator}<${msg.author.id}> requested this bot's token and it was not sent to them because they did not have the required permission`);
        bot.createMessage(msg.channel.id,":x: You don't have the required permission. This incident has been logged. :x:");
    }else if(procmsg(msg,["eris.stop","all.stop","eris.close","all.close","eris.exit","all.exit","eris.logout","all.logout","eris.end","all.end","eris.kill","all.kill"],true,false)){
        await bot.createMessage(msg.channel.id,"Goodbye!");
        process.exit(0);
    }else if(procmsg(msg,["eris.ver","all.ver","eris.version","all.version"])){
        var cont=`\`\`\`\nNodeJs Version:                   ${nodever}\nEris Version:                     ${erisver}\n\`\`\``;
        bot.createMessage(msg.channel.id,cont);
    }else if(msg.content.startsWith("eris.eval")&&is_owner(msg)){
        await evalcmd(msg.content).then(async out=>bot.createMessage(msg.channel.id,out)).catch(console.error);
    }else if(msg.content.startsWith("eris.tst")||msg.content.startsWith("all.tst")) {
        bot.createMessage(msg.channel.id,"I'm up!");
    }
});
bot.connect();
