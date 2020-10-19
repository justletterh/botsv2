f=open('.env',"r+")
dat=f.read()
f.close()
dat=dat.split("\n")
o=[]
for i in dat:
  o.append(f"{i.split('=')[0]}=h")
f=open(".env","w+")
f.write("\n".join(o))
f.close()
print("Done!!!")