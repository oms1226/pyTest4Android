#!/usr/bin/python
# -*- coding: cp949 -*-
import sys

import websocket#websocket-client2 로 설치함!
import _thread as thread
import time
import string
import random
reload(sys)
sys.setdefaultencoding('utf8')

myid=9999
spam=''
seq=['ㅎㅇㅇㅈ','몇살?','25','어디살아?','직업?','지금뭐해?','ㅇㅇ ㅂㅇ']
count=0

def id(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def resp(ws, message=' '):
    global myid,count,spam
    print(str(message.startswith(':')) +" " + str(message.find(str(myid))<0) +" " + str(message.find('!)*')<0))
    if message.startswith('LS'):
        myid=int(message.replace('LS','').split('|')[0])
        print("myid2:"+str(myid))
        return
    elif message.startswith(':') and message.find(str(myid))<0:
        print("Ready to send!"+str(count))
        ws.send("#!)*")
        time.sleep(1)
        ws.send("#"+seq[count])    
        count=count+1
        if(count>=len(seq)):
            ws.close()
            time.sleep(5)

def on_message(ws, message):
    if message.find('!)*')>0:
        return
    elif message.startswith('G'):
        print("MSG:"+message)
        response='#'+str(int(message[-4]))+str(int(message[-3]))+str(int(message[-2]))+str(int(message[-1]))
        print(response)
        ws.send(response)
    print("MSG:"+message)
    resp(ws, message)

def on_error(ws, error):
    print("ERR:"+error)

def on_close(ws):
    print("### closed ###")


conid=id()
rnd=str(random.randrange(100,999))

def on_open(ws):
    global myid,count
    myid=9999
    count=0
    def run(*args):
        ws.send(conid)        
        ws.send("L손님_"+rnd+"|@@@randomchat")
        print("thread opened...id:"+rnd)
    thread.start_new_thread(run, ())


websocket.enableTrace(False)
ws = websocket.WebSocketApp("ws://rchat.gagalive.kr:8082/",
                          on_message = on_message,
                          on_error = on_error,
                          on_close = on_close)
ws.on_open = on_open
ws.run_forever()