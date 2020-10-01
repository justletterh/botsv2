from subprocess import Popen as popen
from subprocess import PIPE as pipe
from json import loads as jload
from os import environ as  env
from threading import Thread as thread
from num2words import num2words as n2w
from sys import stdout
def cap(s):
    o=0
    #0 none,1 start,2 end,3 both 
    if s.startswith(" ") and not s.endswith(" "):
        s=s[1:len(s)]
        o=1
    elif not s.startswith(" ") and s.endswith(" "):
        s=s[0:len(s)-1]
        o=2
    elif s.startswith(" ") and s.endswith(" "):
        s=s[1:len(s)-1]
        o=3
    if " " in s:
        sl=s.split(" ")
        sc=0
        for w in sl:
            sl[sc]=cap(w)
            sc=sc+1
        s=" ".join(sl)
    else:
        s=s.capitalize()
    if o==0:
        return s
    elif o==1:
        return f" {s}"
    elif o==2:
        return f"{s} "
    elif o==3:
        return f" {s} "