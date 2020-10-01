from imports import *
def run_bot(t,c):
    process=popen(['python3','-u','/app/bot.py',t],stdout=pipe,universal_newlines=True)
    while True:
        output = process.stdout.readline()
        if output.strip()!='':
            print(f"[Bot {cap(n2w(c))}]>{output.strip()}")
        return_code=process.poll()
        if return_code is not None:
            o[c]=True
            for output in process.stdout.readlines():
                print(f"[Bot {cap(n2w(c))}]>{output.strip()}")
            break
def main():
    global o,threads
    tokens=jload(env['DISCORD_TOKENS'])
    o=[]
    threads=[]
    c=0
    for t in tokens:
        if t.lower()!="pass":
            o.append(False)
            threads.append(((thread(target=run_bot,args=(t,c))),c))
            threads[c][0].start()
        else:
            o.append(True)
            threads.append((None,None))
        c=c+1
    while not all(o):
        pass
if __name__=="__main__":
    main()