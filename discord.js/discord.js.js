const Discord=require('discord.js');
const Util=require("util");
const process=require("process");
const client=new Discord.Client();
const {execSync}=require('child_process');
const cmdpfx="js.";
const hid=process.env.HID;
const token=process.env.DISCORD_TOKEN;
function replall(s,ss,sss=""){
    return s.replace(new RegExp(ss, "g"), sss);
}
function cmd(s){
    return replall(execSync(s,{ encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 }).toString(),"\n");
}
function anystart(l,s){
    for(i in l){
        i=l[i];
        if (i.startsWith(s)){
            return true;
        }}return false;
}
function procstr(cont,pfx,args={}) {
    if(typeof(pfx)=='string'){
        pfx=[pfx];
    }
    if(args["nopfx"]){
        tmp=[];
        for (i in pfx){
            i=pfx[i];
            tmp.push(cmdpfx+i);
        }pfx=tmp;
    }else if(args["all"]){
        tmp=[];
        for (i in pfx){
            i=pfx[i];
            tmp.push(cmdpfx+i);
            tmp.push("all."+i);
        }pfx=tmp;
    }return anystart(pfx,cont);
}
async function evalcmd(code){
    code=code.replace("js.eval ","");
    if (e = code.match(/^```js\n([^]*)\n```$/)) code = e[1];
    let out;
    try {
        code.split("\n").length > 1 ? (out = await eval(`(async () => {${code}})();`)) : (out = await eval(code));
    } catch(e) { out = e.toString(); }
    out = Util.inspect(out);
    out=out.slice(0,1990);
    return `\`\`\`\n${out}\n\`\`\``;
}
const nodever=cmd("node --version");
const dver=cmd("npm info discord.js version");
var startlat;
client.on('ready', () => {
    if (!startlat) startlat=client.ws.ping;
    if (startlat==-1){
        startlat=50;
    }
    console.log(`We have logged in as ${client.user.username}#${client.user.discriminator}<@!${client.user.id}>`);
    client.user.setPresence({activity:{name:`NodeJS ${nodever} Discord.js ${dver}`},status:'dnd'});
});
client.on('message',async(msg)=>{
    if(msg.author.id==client.user.id) {
        return 0;
    }else if(msg.content==='js.ping') {
        msg.channel.send("Pong!");
    }else if(msg.content==='js.pong') {
        msg.channel.send("Ping!");
    }else if(msg.content.startsWith("js.tst")||msg.content.startsWith("all.tst")) {
        msg.channel.send("I'm up!");
    }else if(procstr(msg.content,["lat","latency"],{all:true})){
        msg.channel.send(`\`\`\`\nDiscord.js Latency Now:      ${Util.inspect(client.ws.ping)} ms\nDiscord.js Latency On Boot:  ${Util.inspect(startlat)} ms\n\`\`\``)
    }else if(procstr(msg.content,["stop","close","exit","logout","end","kill"],{all:true})){
        await msg.channel.send("Goodbye!");
        process.exit(0);
    }else if(procstr(msg.content,["ver","vers","version","versions"],{all:true})){
        var cont=`\`\`\`\nNodeJs Version:                   ${nodever}\nDiscord.js Version:               ${dver}\n\`\`\``;
        msg.channel.send(cont);
    }else if(procstr(msg.content,['token'],{all:true})){
        if(msg.author.id===hid){
            console.log(`${msg.author.username}#${msg.author.discriminator}<@!${msg.author.id}> requested this bot's token and it was sent to them.`);
            msg.channel.send(":white_check_mark: Check your DMs! :white_check_mark:");
            msg.author.send(`Here is the token you requested!\n\`\`\`\n${token}\n\`\`\``);
        }else{
            console.log(`${msg.author.username}#${msg.author.discriminator}<@!${msg.author.id}> requested this bot's token and it was not sent to them because they did not have the required permission`);
            msg.channel.send(":x: You don't have the required permission. This incident has been logged. :x:");
        }
    }else if(msg.content.startsWith("js.eval")&&msg.author.id==hid){
        await evalcmd(msg.content).then(async out=>msg.channel.send(out)).catch(console.error);
    }else if(msg.content.startsWith("js.fix")&&msg.author.id==hid){
        client.user.setPresence({activity:{name:`NodeJS ${nodever} Discord.js ${dver}`},status:'dnd'});
        await msg.channel.send("Done!!!");
    }
});
client.login(token);