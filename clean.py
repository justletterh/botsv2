f=open("docker-compose.yml","r+")
dat=f.read()
f.close()
dat=dat.split("\n")
ss="DISCORD_TOKEN="
out=[]
for i in dat:
  if ss in i:
    i=i.replace(i[i.find(ss)+len(ss):len(i)-1],"tokeypokey")
  out.append(i)
f=open("clean.yml","w+")
f.write("\n".join(out))
f.close()
print("Done!!!")