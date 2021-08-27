import threading
import requests
import time
import random
def hello(i):
    r= requests.get('http://localhost:9001/')
    return r.text,i

for i in range (100):
    time.sleep(random.randint(5,15))
    t= threading.Thread(target=hello,args=(i,))
    t.start()