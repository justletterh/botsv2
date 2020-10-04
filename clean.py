import yaml
f=open("docker-compose.yml","r+")
dat=yaml.safe_load(f.read())
f.close()
for i in dat['services']:
    oi=i
    i=dat['services'][i]
    count=0
    for ii in i['environment']:
        if ii.startswith("DISCORD_TOKEN="):
            dat['services'][oi]['environment'][count]='"DISCORD_TOKEN=bot_token_goes_here"'
        count=count+1
f=open("out.yml","w+")
f.write(yaml.dump(dat))
f.close()
print("Done!!!")