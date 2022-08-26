import sys
import cv2
import os
from stream import RealsenseStream
import numpy as np
import json
from transport import Transport
import asyncio  
from queue import Queue
from threading import Thread, Event
  
# Object that signals shutdown
_sentinel = object()


sockets = []

q1 = Queue()
q2 = Queue()

event = Event()

def stream_to_clients(queue1, queue2, event):
    loop = asyncio.new_event_loop()
    while 1:
        try:
            data1 = queue1.get()
            data2 = queue2.get()
            if(data1 and data2):
                for ws in sockets:
                    try:
                        if(data1):
                            loop.run_until_complete(ws.send(data1))
                        loop.run_until_complete(ws.send(data2))
                    except Exception as e:
                        print(e)

                    event.set()
     
        except Exception as e:
            print(e)
            print(loop)
            

if __name__ == "__main__":
    print("SUBPROCESS_READY")
    stream = RealsenseStream()
    try:
        streaming = Thread(target = stream.start_stream, args =(q1, q2, event), daemon=True)
        streaming.start()
        Thread(target = stream_to_clients, args =(q1, q2, event), daemon=True).start()

        Transport(sys.argv[1], lambda ws:sockets.append(ws), lambda ws:sockets.remove(ws))
        
    except Exception as er:
            print(er)
    finally:
        stream.stop_stream()
        streaming.terinate()
