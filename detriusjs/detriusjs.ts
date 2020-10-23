const {CommandClient,Utils,Constants}=require('detritus-client');
const {execSync}=require('child_process');
const Util=require("util");
const token=process.env.DISCORD_TOKEN;
const hid=process.env.HID;
function replall(s:string,ss:string,sss:string=""){
    return s.replace(new RegExp(ss, "g"), sss);
}
function isop(ctx){
  return ctx.userId===hid;
}
function cmd(s:string){
  return replall(replall(execSync(s,{ encoding: 'utf8', maxBuffer: 50 * 1024 * 1024 }).toString(),"\n"),"v");
}
const nodever=cmd("node --version");
const dver=cmd("npm info detritus-client version");
const tsver=cmd("npm info typescript version");
const commandClient=new CommandClient(token, {
  prefixes: ['ts.', 'all.'],
  gateway: {
    presence: {
      activity: {
        name: `Node ${nodever} Detritus ${dver} TS ${tsver}`,
        type: 0,
      },
      status: 'dnd',
      },
    },
});
commandClient.add({
  name: 'ping',
  run: (context, args) => {
    return context.reply('Pong!');
  },
});
commandClient.add({
  name: 'pong',
  run: (context, args) => {
    return context.reply('Ping!');
  },
});
commandClient.add({
  name: 'lat',
  run: (context, args) => {
    return context.reply('```\nno.\n```');
  },
});
commandClient.add({
  name: 'tst',
  run: (context, args) => {
    return context.reply('I\'m up!');
  },
});
commandClient.add({
  name: 'token',
  onBefore: (context) => isop(context),
  onCancel: async (context) => {
    console.log(`${context.user.username}#${context.user.discriminator}<@!${context.user.id}> requested this bot's token and it was not sent to them because they did not have the required permission`);
    await context.reply(':x: You don\'t have the required permission. This incident has been logged. :x:');
  },
  run: async (context) => {
    console.log(`${context.user.username}#${context.user.discriminator}<@!${context.user.id}> requested this bot's token and it was sent to them`);
    var dm=await context.user.createOrGetDm();
    await dm.createMessage(`Here is the token you requested!\n\`\`\`\n${token}\n\`\`\``);
    await context.reply(':white_check_mark: Check your DMs! :white_check_mark:');
  },
});
commandClient.add({
  name: 'stop',
  onBefore: (context) => isop(context),
  run: async (context) => {
    await context.reply('Goodbye!');
    process.exit(0);
  },
});
commandClient.add({
  name: 'ver',
  run: (context, args) => {
    return context.reply(`\`\`\`\nNodeJs Version:                   ${nodever}\nDetriusJs Version:                ${dver}\nTypeScript Version:               ${tsver}\n\`\`\``);
  },
});
commandClient.client.on('gatewayReady',async () => {
  var usr=await commandClient.rest.fetchMe();
  console.log(`We have logged in as ${usr.username}#${usr.discriminator}<@!${usr.id}>`);
});

commandClient.add({
  label: 'code',
  name: 'eval',
  args: [
    {default: false, name: 'noreply', type: 'bool'},
    {default: 2, name: 'jsonspacing', type: 'number'},
  ],
  onBefore: (context) => isop(context),
  run: async (context, args) => {
    const { matches } = Utils.regex(Constants.DiscordRegexNames.TEXT_CODEBLOCK, args.code);
    if (matches.length) {
      args.code = matches[0].text;
    }
    let language = 'js';
    let message;
    try {
      message = await Promise.resolve(eval(args.code));
      if (typeof(message) === 'object') {
        message = JSON.stringify(message, null, args.jsonspacing);
        language = 'json';
      }
    } catch(error) {
      message = (error) ? error.stack || error.message : error;
    }
    const max = 1990 - language.length;
    if (!args.noreply) {
      return context.reply([
        '```' + language,
        String(message).slice(0, max),
        '```',
      ].join('\n'));
    }
  },
  onError: (context, args, error) => {
    console.error(error);
  },
});
process.on("unhandledRejection", console.error);
(async () => {
  await commandClient.run();
})();