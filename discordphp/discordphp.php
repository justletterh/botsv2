<?php
include '/vendor/autoload.php';
use Discord\DiscordCommandClient;
$token=getenv("DISCORD_TOKEN");
$hid=getenv("HID");
$discord = new DiscordCommandClient([
    'token' => $token,
    'prefix' => 'php.',
    'defaultHelpCommand' => false,
    'discordOptions' => [
        'loggerLevel' => 'ERROR',
        'pmChannels' => true,
    ],
]);
$phpver=explode('.',phpversion())[0].".".explode('.',phpversion())[1].".".explode('-',explode('.',phpversion())[2])[0];
$discver="5.0";
function startswith($haystack, $needle) {
	return $needle === "" || strrpos($haystack, $needle, -strlen($haystack)) !== false;
}
$ping=function($m){
    $m->channel->sendMessage('Pong!');
};
$pong=function($m){
    $m->channel->sendMessage('Ping!');
};
$tst=function($m){
    $m->channel->sendMessage('I\'m up!');
};
$stop=function($m){
    global $discord,$hid;
    if ($m->author->id==$hid){
        $m->channel->sendMessage('Goodbye!')->then(function($nm) use ($discord){
            $discord->close();
        });
    }
};
$lat=function($m){
    $m->channel->sendMessage("```\nno.\n```");
};
$ver=function($m) use ($phpver,$discver){
    $m->channel->sendMessage("```\nPHP Version:                      $phpver\nDiscordPHP Version:               $discver\n```");
};
$toke=function($m) use ($hid,$token){
    if ($m->author->id==$hid){
        $m->channel->sendMessage(':white_check_mark: Check your DMs! :white_check_mark:');
        $m->author->user->sendMessage("Here is the token you requested!\n```\n".$token."\n```");
        echo $m->author->username.'#'.$m->author->discriminator.'<@!'.$m->author->id.'> requested this bot\'s token and it was sent to them'.PHP_EOL;
    }else{
        $m->channel->sendMessage(':x: You don\'t have the required permission. This incident has been logged. :x:');
        echo $m->author->username.'#'.$m->author->discriminator.'<@!'.$m->author->id.'> requested this bot\'s token and it was not sent to them because they did not have the required permission'.PHP_EOL;
    }
};
$fix=function($m) use ($hid,$discord,$phpver,$discver){
    if ($m->author->id==$hid){
        $activity = $discord->factory(\Discord\Parts\User\Activity::class, [
            'type' => 0,
            'name' => 'PHP '.$phpver.' DiscordPHP '.$discver,
        ]);
        $discord->updatePresence($activity,false,'dnd');
        $m->channel->sendMessage('Done!');
    }
};
$discord->registerCommand('ping',$ping);
$discord->registerCommand('pong',$pong);
$discord->registerCommand('tst',$tst);
$discord->registerCommand('stop',$stop);
$discord->registerCommand('lat',$lat);
$discord->registerCommand('ver',$ver);
$discord->registerCommand('token',$toke);
$discord->registerCommand('fix',$fix);
$discord->on('ready', function ($discord) use ($phpver,$discver) {
    echo "We have logged in as ",$discord->username,"#",$discord->discriminator,"<@!",$discord->id,">",PHP_EOL;
    $activity = $discord->factory(\Discord\Parts\User\Activity::class, [
        'type' => 0,
        'name' => 'PHP '.$phpver.' DiscordPHP '.$discver,
    ]);
    $discord->updatePresence($activity,false,'dnd');
    $discord->on('message', function ($message) {
        global $discord,$ping,$pong,$tst,$stop,$lat,$ver,$toke;
        if ($message->author->id!=$discord->id){
            if(startswith($message->content,"all.ping")){
                $ping($message);
            }elseif(startswith($message->content,"all.pong")){
                $pong($message);
            }elseif(startswith($message->content,"all.tst")){
                $tst($message);
            }elseif(startswith($message->content,"all.stop")){
                $stop($message);
            }elseif(startswith($message->content,"all.lat")){
                $lat($message);
            }elseif(startswith($message->content,"all.ver")){
                $ver($message);
            }elseif(startswith($message->content,"all.token")){
                $toke($message);
            }
          }
    });
});
$discord->run();
?>